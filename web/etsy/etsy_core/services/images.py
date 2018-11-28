from ..models import ProductImage, Product


class ProductImageHandler:
    @staticmethod
    def add_image_to_product(image, product_id):
        product = Product.objects.get(id=product_id)
        ProductImage.objects.create(product=product, image=image)
