from django.contrib import admin
from .models import Carro, Marca, ImagemSite


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ['nome', 'ativa', 'ordem']
    list_filter = ['ativa']
    search_fields = ['nome']
    list_editable = ['ativa', 'ordem']
    
    fieldsets = (
        ('Informações da Marca', {
            'fields': ('nome', 'logo', 'ativa', 'ordem')
        }),
    )


@admin.register(Carro)
class CarroAdmin(admin.ModelAdmin):
    list_display = ['fabricante', 'modelo', 'ano', 'preco', 'condicao', 'destaque', 'criado_em']
    list_filter = ['fabricante', 'condicao', 'destaque', 'ano']
    search_fields = ['modelo', 'fabricante', 'descricao']
    list_editable = ['destaque', 'condicao']
    readonly_fields = ['criado_em', 'atualizado_em']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('modelo', 'fabricante', 'ano', 'cor')
        }),
        ('Detalhes Técnicos', {
            'fields': ('quilometragem', 'combustivel', 'cambio', 'motor')
        }),
        ('Informações Comerciais', {
            'fields': ('preco', 'condicao', 'destaque')
        }),
        ('Descrição e Imagens', {
            'fields': ('descricao', 'imagem_principal', 'imagem_2', 'imagem_3', 'imagem_4')
        }),
        ('Metadados', {
            'fields': ('criado_em', 'atualizado_em'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ImagemSite)
class ImagemSiteAdmin(admin.ModelAdmin):
    list_display = ['nome', 'tipo', 'ativo', 'ordem', 'data_criacao', 'preview_image']
    list_filter = ['tipo', 'ativo', 'data_criacao']
    search_fields = ['nome', 'descricao']
    list_editable = ['ativo', 'ordem']
    readonly_fields = ['data_criacao', 'preview_image']
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'tipo', 'imagem', 'ativo')
        }),
        ('Detalhes', {
            'fields': ('descricao', 'ordem')
        }),
        ('Preview & Sistema', {
            'fields': ('preview_image', 'data_criacao'),
            'classes': ('collapse',)
        }),
    )
    
    def preview_image(self, obj):
        """Mostra preview da imagem no admin"""
        if obj.imagem:
            return f'<img src="{obj.imagem.url}" style="max-width: 150px; max-height: 100px;" />'
        return "Sem imagem"
    preview_image.allow_tags = True
    preview_image.short_description = "Preview"
    
    class Media:
        css = {
            'all': ('admin/css/forms.css',)
        }
