from kandinsky2 import get_kandinsky2

# class generate lists of images based on ruDall-e Kandinsky 2.0
class Imaginator:
    def __init__(self):
        model = get_kandinsky2('cuda', task_type='text2img')
    
    #input: text - list of strings, spec - str with specification(e.g. 'Van Gog like' etc)
    #return: None. Saving generated images into ./../data/tmp_imgs/
    def getImages(text: list, spec: str):
        for i, value in enumerate(text):
            image = model.generate_text2img(f'{value}, {spec}', batch_size=1, h=512, w=512, 
                                            num_steps=75, denoised_type='dynamic_threshold', dynamic_threshold_v=99.5, 
                                            sampler='ddim_sampler', ddim_eta=0.01, guidance_scale=10)
            image[0].save(f'./../data/tmp_imgs/img{i}.jpg')