from django.contrib import admin
from .models import Product
from django.shortcuts import render, redirect
from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.urls import path

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):

    list_display = "pk", "name", 'description', "price",
    list_display_links = "pk", "name"
    ordering = "pk", "name"
