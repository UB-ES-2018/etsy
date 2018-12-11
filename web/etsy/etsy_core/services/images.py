from ..models import ProductImage, Product


class ProductImageHandler:
	@staticmethod
	def add_image_to_product(image, product_id):
		product = Product.objects.get(id=product_id)
		ProductImage.objects.create(product=product, image=image)
		if not product.creation_finished:
			product.creation_finished = True
			product.save()

	@staticmethod
	def remove_all_product_images(product_id):
		product = Product.objects.get(id=product_id)
		ProductImage.objects.filter(product=product).delete()
		product.creation_finished = False
		product.save()
