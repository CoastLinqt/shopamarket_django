from django.contrib import admin
from .models import Categories
from shopapp.models import Sales
from django.shortcuts import render, redirect
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import path


@admin.register(Categories)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "title",
    )
    list_display_links = "pk", "title"
    ordering = "pk", "title"


@admin.register(Sales)
class SalesAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "salePrice",
        "dateFrom",
        "dateTo",
        "product",
    )
    list_display_links = ("pk",)
    ordering = ("pk",)
