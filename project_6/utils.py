import pandas as pd
import numpy as np

# %matplotlib ipympl
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['figure.dpi'] = 300
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D

import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

import warnings 

from IPython.display import display, HTML

warnings.filterwarnings("ignore")

plt.rcParams["patch.force_edgecolor"] = True

import pickle

import cupy as cp

from cuml import UMAP, TSNE
from cuml.decomposition import PCA
from cuml.preprocessing import StandardScaler, MinMaxScaler
from cuml.cluster import KMeans, AgglomerativeClustering, DBSCAN, HDBSCAN
from cuml.model_selection import GridSearchCV

from sklearn.metrics import calinski_harabasz_score, davies_bouldin_score

import time



class DataLoader():
    def __init__(
        self,
        descriptor_names = [
            'efficientnet-b7', 'osnet', 'vdc_color', 'vdc_type'
        ],
        descriptor_folder = 'data/descriptors/',
        image_paths = 'data/images_paths.csv',
        verbose:bool = True,
    ):
        """Class for data loading (descriprots and image_paths)

        Args:
            descriptor_names (list): List of descriptor names. Defaults to 
                ['efficientnet-b7', 'osnet', 'vdc_color', 'vdc_type'].
            descriptor_folder (str, optional): Folder where descriptors kept. 
                Defaults to 'data/descriptors/'.
            image_paths (str, optional): Path to "image_paths" dataset. 
                Defaults to 'data/images_paths.csv'.
            verbose (bool): Print additional messages. Defaults to True
            
        """
        self._descriptor_folder = descriptor_folder
        self.descriptor_names = descriptor_names
        self.full_image_paths = pd.read_csv(image_paths)
        self._descriptor = None
        self._descriptor_name = None
        self._image_paths = None
        self.verbose = verbose
        if self.verbose:
            # Show image paths details
            print('Shape of "image paths":', self.full_image_paths.shape)
            display(self.full_image_paths.head())
    
    def __del__(self):
        del self._descriptor
    
    def _load_full_descriptor(self, name:str, dtype:str='cupy'):
        """Load descriptor with stated "name" in RAM or GPU (see "dtype")

        Args:
            name (str): Name of the descriptor to load
            dtype (str): Select type of data:
            - 'numpy' - numpy.ndarray format (keep data on RAM);
            - 'cupy' - cupy.ndarray format (keep data on GPU).
            Defaults to 'cupy'.

        Raises:
            TypeError: If data type is not in ["numpy", "cupy"]
        """
        with open(
            self._descriptor_folder + name + '.pickle',
            'rb' # read binary
        ) as pkl_file:
            self._descriptor = pickle.load(pkl_file)
            self._descriptor_name = name
            if dtype.strip().lower() == 'numpy':
                pass
            elif dtype.strip().lower() == 'cupy':
                self._descriptor = cp.asarray(self._descriptor)
            else:
                raise TypeError(
                    'Wrong data_type. Only "numpy" and "cupy" allowed'
                )
        self._image_paths = self.full_image_paths
    
    
    def load_descriptor(
        self, 
        name:str,
        dtype:str='cupy',
        data_fraction:float=1.0,
        random_state:int=None,
    ):
        """Load random part of the descriptor with stated "name" in RAM 
        or GPU (see "dtype") and with setted fraction. 
        If data_fraction==1.0, load full descriptor.

        Args:
            name (str): Name of the descriptor to load
            dtype (str): Select type of data:
            - 'numpy' - numpy.ndarray format (keep data on RAM);
            - 'cupy' - cupy.ndarray format (keep data on GPU).
            Defaults to 'cupy'.
            data_fraction (float): Fraction of the descriptor to load. 
                Defaults to 1.0.
            random_state (int, optional): Set random state for the random 
                generator. Defaults to None.

        Raises:
            ValueError: Data fraction must be in the range [0, 1]
        """
        if data_fraction < 0.0 or data_fraction > 1.0:
            raise ValueError('data_fraction must be in the range [0, 1]')
        
        self._load_full_descriptor(name, dtype)
        
        if data_fraction == 1.0:
            if self.verbose:
                print('All dataset downloaded')
            return
        
        # Get required row count
        row_cnt = np.ceil(
            data_fraction * self._descriptor.shape[0]
        ).astype(int)
        
        rng = np.random.default_rng(random_state)
        indexes = rng.choice(
            self._descriptor.shape[0], 
            size=row_cnt,
            replace=False
        )
        indexes.sort()
        
        # Save active descriptor and related image paths
        self._descriptor = self._descriptor[indexes,:]
        self._image_paths = self.image_paths.iloc[indexes,:]
        
    
    @property
    def descriptor(self):
        """Return active descriptor and its name

        Returns:
            typle: (descriptor name, descriptor)
        """
        return (self._descriptor_name, self._descriptor)
    
    
    @property
    def image_paths(self):
        return self._image_paths
    
    
    def print_descriptor_info(self):
        """Print active descriptor name and shape
        """
        descriptor_name, descriptor = self.descriptor
        print(f'Descriptor "{descriptor_name}":')
        print(f'\tShape: {descriptor.shape}')



class DataKeeper():
    def __init__(
        self,
        n_components_dict:dict = {
            "efficientnet-b7": 250,
            "osnet": 150,
            "vdc_color": 100,
            "vdc_type": 150,
        },
        loader_verbose = False,
    ):
        """DataKeeper keeps active PCA-reduced descriptor 
        and its Standard- and Norm- scaled version

        Args:
            n_components_dict (dict): Number of PCA-components 
            for each dataframe. Defaults to {
                    "efficientnet-b7": 250, 
                    "osnet": 150, 
                    "vdc_color": 100, 
                    "vdc_type": 150, 
                }.
            loader_verbose (bool): Print additional information. 
                Defaults to False.
        """
        self.loader = DataLoader(verbose=loader_verbose)
        self.n_components_dict = n_components_dict
        
        self.del_data() # Prepare empty data variables
    
    
    def del_PCA(self):
        """Clean PCA
        """
        # descriptor_PCA
        self.descriptor_PCA = None
        self.pca:PCA = None
    
    
    def del_data(self):
        """Clean data variables
        """
        self.del_PCA()
        
        self.descriptors_scaled = {}
        
        # StandardScaler
        # self.descriptor_std = None
        self.std_scaler = None
        
        # MinMaxScaler
        # self.descriptor_norm = None
        self.norm_scaler = None
        
    
    def get_PCA_descriptor(
        self,
        random_state:int=None,
    ):
        """Get descriptor with reduced features (by PCA)

        Args:
            random_state (int): Random state for the PCA. Defaults to None.
        """
        self.pca = PCA(
            n_components=self.n_components_dict[
                self.loader._descriptor_name
            ], 
            random_state=random_state
        )
        self.descriptor_PCA = self.pca.fit_transform(
            self.loader._descriptor
        )
        # Free space of the original desciptor
        self.loader._descriptor = None
        
    
    def load_descriptor_PCA(
        self, 
        name:str,
        data_fraction:float=1.0,
        random_state:int=None,
    ):
        """Load descriptor by self.loader.load_descriptor and get PCA

        Args:
            name (str): Name of the descriptor to load
            data_fraction (float): Fraction of the descriptor to load.
                Defaults to 1.0.
            random_state (int, optional): Set random state for the random 
                generator and PCA. Defaults to None.
        """
        self.loader.load_descriptor(
            name, 
            data_fraction=data_fraction, 
            random_state=random_state
        )
        self.get_PCA_descriptor(random_state=random_state)
 
   
    def get_std_scaled_descriptor(self):
        """Get Standard scaled data
        """
        self.std_scaler = StandardScaler()
        self.descriptors_scaled['std'] = self.std_scaler.fit_transform(
            self.descriptor_PCA
        )
    
    
    def get_norm_scaled_descriptor(self):
        """Get MinMax scaled data
        """
        self.norm_scaler = MinMaxScaler()
        self.descriptors_scaled['norm'] = self.norm_scaler.fit_transform(
            self.descriptor_PCA
        )
    
    
    # def get_scaled_descriptors(
    #     self,
    # ):
    #     """Get Norm- and Standard- scaled data
    #     """
    #     self.get_norm_scaled_descriptor()
    #     self.get_std_scaled_descriptor()



def conduct_grid_search(
    selected_params:dict,
    get_mesh=True,
    scaler: list = ['norm', 'std'],
    data_keeper:DataKeeper=DataKeeper(),
    data_fraction:float = 0.5,
    random_state:int = 42,
    delay:float = 0.1,
):
    """Conduct Grid Search according to the selected_params.

    Args:
        selected_params (dict): Descriptor - ModelClass - 
            dict of Class params for searching
        get_mesh (bool): Mesh grid or not. Defaults to True.
        scaler (list): List of scalers to conduct grid search
        data_keeper (DataKeeper): Obj to get descriptors. 
            Defaults to data_keeper.
        data_fraction (float): Fraction of the descriptor to load. 
            Defaults to 1.0.
        random_state (int, optional): Set random state for the random 
            generator. Defaults to None.
        delay (float): Time delay while class is cleaning

    Returns:
        list: Cluster grid Search results
    """
    
    cluster_results = []

    for descriptor_name in selected_params:
        print(f'ДЕСКРИПТОР {descriptor_name}')
        # Free memory from datasets
        data_keeper.del_data() 
        
        # Load descriptor
        data_keeper.load_descriptor_PCA(
            name=descriptor_name,
            data_fraction=data_fraction,
            random_state=random_state,
        )
        # Scale descriptor
        if 'norm' in scaler:
            data_keeper.get_norm_scaled_descriptor()
        if 'std' in scaler:
            data_keeper.get_std_scaled_descriptor()
        data_keeper.del_PCA() # Free up memory from PCA
        
        
        for cluster_class in selected_params[descriptor_name]:
            print(f'Модель кластеризации: {cluster_class.__name__}')
            for scaler_name in data_keeper.descriptors_scaled:
                print(f'Метод масштабирования: {scaler_name}')
                # Prepare Data and params dict
                X = data_keeper.descriptors_scaled[scaler_name]
                params_dict = selected_params[descriptor_name][cluster_class]
                
                if get_mesh:
                    # Get parameters combination
                    mesh = np.meshgrid(
                        *list(params_dict.values())
                    )
                    params = np.hstack([x.reshape(-1, 1) for x in mesh])
                else:
                    # If mesh does not required - construct columns
                    params = np.hstack(
                        [
                            np.array(x).reshape(-1,1) 
                                for x in params_dict.values()
                        ]
                    )

                for param_row in params:
                    current_params = {}
                    # Get parameters dict from the parameters combination row
                    for i, key in enumerate(params_dict):
                        current_params[key] = param_row[i]
                    
                    print(current_params, end=' ...')
                    # Init clust. model with curret params combination
                    cluster_model = cluster_class(**current_params)
                    cluster_model.fit(X)
                    n_clusters = len(np.unique(cluster_model.labels_))
                    if n_clusters >= 2:
                        ch_score = calinski_harabasz_score(
                            X.get(), 
                            cluster_model.labels_.get()
                        )
                        db_score = davies_bouldin_score(
                            X.get(), 
                            cluster_model.labels_.get()
                        )
                    else:
                        ch_score = None
                        db_score = None
                    
                    cluster_results.append(
                        {
                        'descriptor': descriptor_name,
                        'scaler': scaler_name,
                        'cluster_class': cluster_class.__name__,
                        'cluster_class_params': current_params,
                        'labels': cluster_model.labels_.get().copy(),
                        'n_clusters': n_clusters,
                        'calinski_harabasz_score': ch_score,
                        'davies_bouldin_score': db_score
                        }
                    )
                    cluster_model = None
                    time.sleep(delay) # Delay for the GPU memory cleaning up
                    cp._default_memory_pool.free_all_blocks()
                    time.sleep(delay) # Delay for the GPU memory cleaning up
                    print('\tDONE!')
            print()
        print()
    
    return cluster_results 


def display_models(full_df):
    """ Display sorted by metric models grouped by descriptor

    Args:
        full_df (pd.DataFrame): DataFrame to eject sorted data
    """
    for descriptor in full_df['descriptor'].unique():
        print(f'ДЕСКРИПТОР: {descriptor}')
        df = full_df[full_df['descriptor'] == descriptor]
        df = df[[
            'cluster_class', 'cluster_class_params', 
            'n_clusters', 'calinski_harabasz_score', 'davies_bouldin_score'
        ]]
        df = df.sort_values(
            ['cluster_class', 'calinski_harabasz_score', 'davies_bouldin_score'],
            ascending=[False, False, True]
        )
        
        display(df)


def countplot_clusters(full_df, sidesize=4):
    """ Plot clusters count

    Args:
        full_df (pd.Dataframe): Dataframe with descriptor, models 
            and obtained clusters
        sidesize (int): Width of the one plot. Defaults to 4.
    """

    for descriptor in full_df['descriptor'].unique():
        df = full_df[full_df['descriptor'] == descriptor]
        fig, axes = plt.subplots(
            (df.shape[0]+1)//2, 2, 
            figsize=(2*sidesize, df.shape[0]//2*sidesize)
        )

        for i in range(df.shape[0]):
            ax = axes.flat[i]
            row = df.iloc[i]
            sns.countplot(
                x = row['labels'],
                ax=ax
            )
            
            row_lt = list(
                row[['descriptor', 'cluster_class', 'cluster_class_params']].values
            )
            row_lt = list(map(str, row_lt))

            row_name = '\n'.join(row_lt)
            
            ax.set_title(row_name)
        plt.tight_layout()