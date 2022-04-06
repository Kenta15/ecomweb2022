from django.urls import path
from . import views


urlpatterns=[
    path('',views.store,name="store"),
    path('grocery/',views.grocery,name="grocery"),
    path('cosmetic/',views.cosmetic,name="cosmetic"),
    path('gaming/',views.gaming,name="gaming"),
    path('electronic/',views.electronic,name="electronic"),
    path('apparel/',views.apparel,name="apparel"),
    path('book/',views.book,name="book"),
    path('daily/',views.daily,name="daily"),
    path('kitchen/',views.kitchen,name="kitchen"),
    path('pet/',views.pet,name="pet"),
    path('health/',views.health,name="health"),
    path('bestseller/',views.bestseller,name="bestseller"),
    path('cart/',views.cart,name="cart"),
    path('checkout/',views.checkout,name="checkout"),
    path('update_item/',views.updateItem,name="update_item"),
    path('process_order/',views.processOrder,name="process_order"),
    path('register/',views.registerPage,name="register"),
    path('login/',views.loginPage,name="login"),
    path('loginout/',views.logoutPage,name="logout"),
    path('country/',views.countryPage,name="country"),
    path('update_country/',views.updateCountry,name="update_country"),
    path('settings/',views.settingPage,name="settings"),
    path('contact/',views.contactPage,name="contact"),
    path('forgot/',views.forgotPage,name="forgot"),
    path('new/',views.newPage,name="new"),
    path('search/',views.searchPage,name="search"),
]