# def save(self, *args, **kwargs):

#     super(Profile, self).save()
#     img = Image.open(self.image)
#     if img.height > 300 or img.width > 300:
#         size = 200, 200
#         fh = storage.open(self.image.name, "w")
#         format = "jpg"  # You need to set the correct image format here
#         img.save(fh, format)
#         fh.close()
# super().save(*args, **kwargs)

# fh = storage.open(self.image.name, "w")
# format = "jpg"  # You need to set the correct image format here
# image.save(fh, format)
# fh.close()
# img = Image.open(self.image.name)
# if img.height > 300 or img.width > 300:
#     output_size = (300, 300)
#     img.thumbnail(output_size)
#     img.save(self.image.name)

# img = Image.open(self.image)
# if img.height > 300 or img.width > 300:
#     output_size = (300, 300)
#     img.thumbnail(output_size)
#     img.save(self.image.name)
#     self.image.save(self.image.name, self.image)
