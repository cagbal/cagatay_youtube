import torch 
import torchvision

class ArkaPlanSilici(object):
    def __init__(self):
        self.model = torchvision.models.segmentation.deeplabv3_resnet50(pretrained=True, progress=True)
        
        self.model.eval()
        
    def tahminleri_filtrele(self, tahminler, sinif=15):
        return tahminler==15
    
    def maskele(self, imge, tahminler):
        return imge*tahminler
    
    def alpha_kanali_ekle(self, imge, alpha):
        alpha=torch.unsqueeze(alpha, 0)
        imge = torch.cat((imge,alpha),0)
        return imge
        
        
    def sil(self, imge):
        imge = torchvision.transforms.Resize(512)(imge)
        
        imge_tensor = torchvision.transforms.ToTensor()(imge)
        
        imge_tensor_normalize = torchvision.transforms.Normalize(
            [0.485, 0.456, 0.406], 
            [0.229, 0.224, 0.225])(imge_tensor)
        
        imge_segmentler = self.model(torch.unsqueeze(imge_tensor_normalize, 0))
        
        tahminler = imge_segmentler["out"][0,:,:,:].argmax(0)
        
        tahminler = self.tahminleri_filtrele(tahminler)
        
        imge_filtrelenmis = self.maskele(imge_tensor, tahminler)
        
        imge_filtrelenmis = self.alpha_kanali_ekle(imge_filtrelenmis, tahminler)
        
        return torchvision.transforms.ToPILImage()(imge_filtrelenmis)
    
    
