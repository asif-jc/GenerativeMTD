from ClusterMTD import *
from VAE import *
from GVAE import *
from AE import *
from GAE import *
from GenerativeMTD import *
import torch
from train_options import *
from gvae_data_transformer import *
import neptune
import neptune.new as neptune
from veegan import *
from veegan.veegan import VEEGAN
from tablegan import *
from tablegan.tablegan import TableGAN
import utils
from ast import literal_eval
from preprocess import find_cateorical_columns, match_dtypes





def train_GVAE(opt):
    run = neptune.init(project="jaysivakumar/G-VAE", api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIzZTE3OWZiNS0xNzkyLTQ0ZjYtYmVjMC1hOWE1NjE4MGQ3MzcifQ==')  # your credentials
    run['config/dataset/path'] = opt.file
    # run['config/dataset/transforms'] = data_tfms # dict() object
    # run['config/dataset/size'] = dataset_size # dict() object
    run['config/model'] = "G-VAE"
    run['config/criterion'] = "MMD + KL"
    run['config/optimizer'] = "Adam"
    # run['config/params'] = hparams # dict() object
    data = LoadFile(opt,run)
    D_in = data.__dim__()
    df,opt = data.load_data()
    opt.class_col = df.columns[opt.target_col_ix]

    opt.cat_col = find_cateorical_columns(df)

    model = GVAE(opt, D_in,run)
    model.fit(df,discrete_columns = opt.cat_col)
    gvae_fake = model.sample(1000)
    run['output/Final PCD'] = utils.PCD(df,gvae_fake)
    kstest, cstest = utils.stat_test(df,gvae_fake)
    run['output/KSTest'] = kstest
    run['output/CSTest'] = cstest
    run['output/TSTR'] = utils.predictive_model(df,gvae_fake,opt.class_col,'TSTR')
    run['output/TRTS'] = utils.predictive_model(df,gvae_fake,opt.class_col,'TRTS')
    run['output/DCR'] = utils.DCR(df,gvae_fake)
    run['output/NNDR'] = utils.NNDR(df,gvae_fake)
    run.stop()

def train_veegan(opt):
    run = neptune.init(project="jaysivakumar/VEEGAN", api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIzZTE3OWZiNS0xNzkyLTQ0ZjYtYmVjMC1hOWE1NjE4MGQ3MzcifQ==')  # your credentials
    run['config/dataset/path'] = opt.file
    # run['config/dataset/transforms'] = data_tfms # dict() object
    # run['config/dataset/size'] = dataset_size # dict() object
    run['config/model'] = "VEEGAN"
    run['config/criterion'] = "MMD + KL"
    run['config/optimizer'] = "SGD"
    # run['config/params'] = hparams # dict() object
    data = LoadFile(opt,run)
    D_in = data.__dim__()
    df,opt = data.load_data()
    opt.class_col = df.columns[opt.target_col_ix]

    opt.cat_col = find_cateorical_columns(df)
    model = VEEGAN(opt,run)
    model.fit(df,categorical_columns = opt.cat_col)
    veegan_fake = model.sample(1000)
    run['output/Final PCD'] = utils.PCD(df,veegan_fake)
    kstest, cstest = utils.stat_test(df,veegan_fake)
    run['output/KSTest'] = kstest
    run['output/CSTest'] = cstest
    run['output/TSTR'] = utils.predictive_model(df,veegan_fake,opt.class_col,'TSTR')
    run['output/TRTS'] = utils.predictive_model(df,veegan_fake,opt.class_col,'TRTS')
    run['output/DCR'] = utils.DCR(df,veegan_fake)
    run['output/NNDR'] = utils.NNDR(df,veegan_fake)
    run.stop()

def train_tablegan(opt):
    run = neptune.init(project="jaysivakumar/TableGAN", api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIzZTE3OWZiNS0xNzkyLTQ0ZjYtYmVjMC1hOWE1NjE4MGQ3MzcifQ==')  # your credentials
    run['config/dataset/path'] = opt.file
    run['config/model'] = "TableGAN"
    run['config/criterion'] = "MMD + KL"
    run['config/optimizer'] = "SGD"
    data = LoadFile(opt,run)
    D_in = data.__dim__()
    df,opt = data.load_data()
    opt.class_col = df.columns[opt.target_col_ix]

    opt.cat_col = find_cateorical_columns(df)
    model = TableGAN(opt,run)
    model.fit(df,categorical_columns = opt.cat_col)
    tablegan_fake = model.sample(1000)
    run['output/Final PCD'] = utils.PCD(df,tablegan_fake)
    kstest, cstest = utils.stat_test(df,tablegan_fake)
    run['output/KSTest'] = kstest
    run['output/CSTest'] = cstest
    run['output/TSTR'] = utils.predictive_model(df,tablegan_fake,opt.class_col,'TSTR')
    run['output/TRTS'] = utils.predictive_model(df,tablegan_fake,opt.class_col,'TRTS')
    run['output/DCR'] = utils.DCR(df,tablegan_fake)
    run['output/NNDR'] = utils.NNDR(df,tablegan_fake)
    run.stop()




if __name__ == "__main__":
    opt = TrainOptions().parse()
    # opt.cat_col = literal_eval(opt.cat_col)
    
    # opt.device = torch.device('cuda:{}'.format(opt.gpu_ids[0])) if opt.gpu_ids else torch.device('cpu') 
    if(opt.model == 'veegan'):
        train_veegan(opt)
    if(opt.model == 'tablegan'):
        train_tablegan(opt)
    # if(opt.model == 'ctgan'):
    #     train_ctgan(opt)
    # if(opt.model == 'copulagan'):
    #     train_copulagan(opt)
    if(opt.model == 'GVAE'):
        train_GVAE(opt)



    # if(opt.model == 'GMTD'):
    #     train_GMTD(opt)
    
    # if(opt.model == 'GAE'):
    #     train_GAE(opt)
    # if(opt.model == 'VAE'):
    #     train_VAE(opt)
    # if(opt.model == 'AE'):
    #     train_AE(opt)
    







####################################################################################
# def train_GMTD(opt):
#     run = neptune.init(project="jaysivakumar/GMTD", api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIzZTE3OWZiNS0xNzkyLTQ0ZjYtYmVjMC1hOWE1NjE4MGQ3MzcifQ==')  # your credentials
#     run['config/dataset/path'] = opt.file
#     # run['config/dataset/transforms'] = data_tfms # dict() object
#     # run['config/dataset/size'] = dataset_size # dict() object
#     run['config/model'] = "G-MTD"
#     run['config/criterion'] = "MMD"
#     run['config/optimizer'] = "Adam"
#     # run['config/params'] = hparams # dict() object
#     data = LoadFile(opt,run)
#     D_in = data.__dim__()
#     df,opt = data.load_data()
#     model = GMTD(opt, D_in,run)
#     model.fit(df,discrete_columns = opt.cat_col)



# def train_GAE(opt):
#     run = neptune.init(project="jaysivakumar/G-AE", api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIzZTE3OWZiNS0xNzkyLTQ0ZjYtYmVjMC1hOWE1NjE4MGQ3MzcifQ==')  # your credentials
#     run['config/dataset/path'] = opt.file
#     # run['config/dataset/transforms'] = data_tfms # dict() object
#     # run['config/dataset/size'] = dataset_size # dict() object
#     run['config/model'] = "G-AE"
#     run['config/criterion'] = "MMD + CORAL + KL"
#     run['config/optimizer'] = "Adam"
#     # run['config/params'] = hparams # dict() object
#     data = LoadFile(opt,run)
#     D_in = data.__dim__()
#     df,opt = data.load_data()
#     opt.cat_col = find_cateorical_columns(df)

#     model = GAE(opt, D_in,run)
#     model.fit(df,discrete_columns = opt.cat_col)


# def train_AE(opt):
#     run = neptune.init(project="jaysivakumar/AutoE", api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIzZTE3OWZiNS0xNzkyLTQ0ZjYtYmVjMC1hOWE1NjE4MGQ3MzcifQ==')  # your credentials
#     run['config/dataset/path'] = opt.file
#     # run['config/dataset/transforms'] = data_tfms # dict() object
#     # run['config/dataset/size'] = dataset_size # dict() object
#     run['config/model'] = "AutoE"
#     run['config/criterion'] = "MMD + CORAL + KL"
#     run['config/optimizer'] = "Adam"
#     # run['config/params'] = hparams # dict() object
#     data = LoadFile(opt,run)
#     D_in = data.__dim__()
#     df,opt = data.load_data()
#     opt.cat_col = find_cateorical_columns(df)

#     model = AE(opt, D_in,run)
#     model.fit(df,discrete_columns = opt.cat_col)


# def train_VAE(opt):
#     run = neptune.init(project="jaysivakumar/VAE", api_token='eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vYXBwLm5lcHR1bmUuYWkiLCJhcGlfdXJsIjoiaHR0cHM6Ly9hcHAubmVwdHVuZS5haSIsImFwaV9rZXkiOiIzZTE3OWZiNS0xNzkyLTQ0ZjYtYmVjMC1hOWE1NjE4MGQ3MzcifQ==')  # your credentials
#     run['config/dataset/path'] = opt.file
#     # run['config/dataset/transforms'] = data_tfms # dict() object
#     # run['config/dataset/size'] = dataset_size # dict() object
#     run['config/model'] = "VAE"
#     run['config/criterion'] = "MMD + CORAL + KL"
#     run['config/optimizer'] = "Adam"
#     # run['config/params'] = hparams # dict() object
#     data = LoadFile(opt,run)
#     D_in = data.__dim__()
#     df,opt = data.load_data()
#     opt.cat_col = find_cateorical_columns(df)

#     model = VAE(opt, D_in,run)
#     model.fit(df,discrete_columns = opt.cat_col)