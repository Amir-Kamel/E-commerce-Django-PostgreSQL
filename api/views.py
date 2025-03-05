from rest_framework import viewsets, mixins
from .serializers import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .serializers import ProductSerializer
from .permissions import *
from rest_framework.response import Response
from rest_framework import status

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, OnlyAdminsCanDeletePermission]

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, OnlyAdminsCanDeletePermission]


class CartItemViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):

    def list(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(cart__user=request.user)
        return super().list(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message": "Item deleted successfully"})

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated, IsCartOwner]
    queryset = CartItem.objects.all()









