from django.core.management.base import BaseCommand
from apps.core.models import JobCategory
from django.utils.text import slugify

class Command(BaseCommand):
    help = 'Popula categorias de jobs no sistema'

    def handle(self, *args, **options):
        categories = [
            {'name': 'Desenvolvimento Web', 'icon': '💻'},
            {'name': 'Design Gráfico', 'icon': '🎨'},
            {'name': 'Marketing Digital', 'icon': '📱'},
            {'name': 'Consultoria', 'icon': '💼'},
            {'name': 'Redação', 'icon': '✍️'},
            {'name': 'Tradução', 'icon': '🌐'},
            {'name': 'Vendas', 'icon': '📈'},
            {'name': 'Suporte Técnico', 'icon': '🔧'},
            {'name': 'Análise de Dados', 'icon': '📊'},
            {'name': 'Mobile', 'icon': '📱'},
            {'name': 'DevOps', 'icon': '⚙️'},
            {'name': 'UI/UX Design', 'icon': '🎯'},
            {'name': 'Gestão de Projetos', 'icon': '📋'},
            {'name': 'Recursos Humanos', 'icon': '👥'},
            {'name': 'Financeiro', 'icon': '💰'},
            {'name': 'Educação', 'icon': '📚'},
            {'name': 'Saúde', 'icon': '🏥'},
            {'name': 'Jurídico', 'icon': '⚖️'},
            {'name': 'Pesquisa', 'icon': '🔬'},
            {'name': 'Outros', 'icon': '🔮'},
        ]
        
        created_count = 0
        
        for cat_data in categories:
            slug = slugify(cat_data['name'])
            category, created = JobCategory.objects.get_or_create(
                slug=slug,
                defaults={
                    'name': cat_data['name'],
                    'icon': cat_data['icon']
                }
            )
            
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"✅ Categoria criada: {category.icon} {category.name}")
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f"⚠️  Categoria já existe: {category.icon} {category.name}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f"\n🎉 {created_count} categorias criadas!")
        )
        self.stdout.write(
            self.style.SUCCESS(f"📊 Total de categorias: {JobCategory.objects.count()}")
        )
