from ..models import Options, OptionField, ProductOptions, ProductTags


class VariationsHandler:

	@staticmethod
	def get_default_variations():
		default_options = {}
		options = Options.objects.filter(is_default=True)
		for option in options:
			default_options[(option.id, option.options_name)] = [
				(field.id, field.field_name) for field in OptionField.objects.filter(options_id=option.id)]

		return default_options

	@staticmethod
	def add_variations_to_product(product, variation):
		ProductOptions.objects.create(product=product, options=variation)

	@staticmethod
	def remove_all_product_variations(product):
		ProductOptions.objects.filter(product = product).delete()
	
	@staticmethod
	def add_tag_to_product(product, tag):
		ProductTags.objects.create(product=product, tags=tag)
		
	@staticmethod
	def remove_all_product_tags(product):
		ProductTags.objects.filter(product = product).delete()
