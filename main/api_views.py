from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import GalleryItem, Project
from .permissions import IsPortfolioOwnerOrEditorOrReadOnly, IsPortfolioOwnerOrReadOnly
from .serializers import GalleryItemSerializer, ProjectSerializer


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_list(request):
    if request.method in ("GET", "HEAD"):
        projects = Project.objects.prefetch_related("starred_by").order_by("title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            projects = projects.filter(title__icontains=title)
        return Response(ProjectSerializer(projects, many=True, context={"request": request}).data)
    serializer = ProjectSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrReadOnly])
def project_detail(request, project_id):
    project = get_object_or_404(Project.objects.prefetch_related("starred_by"), pk=project_id)
    if request.method in ("GET", "HEAD"):
        return Response(ProjectSerializer(project, context={"request": request}).data)
    if request.method == "DELETE":
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = ProjectSerializer(project, data=request.data, partial=request.method == "PATCH",
                                   context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def project_star(request, project_id):
    project = get_object_or_404(Project, pk=project_id)
    if project.starred_by.filter(pk=request.user.pk).exists():
        project.starred_by.remove(request.user)
    else:
        project.starred_by.add(request.user)
    return Response(ProjectSerializer(project, context={"request": request}).data)


@api_view(["GET", "HEAD", "POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def gallery_list(request):
    if request.method in ("GET", "HEAD"):
        items = GalleryItem.objects.prefetch_related("starred_by").order_by("-featured", "-year", "title", "id")
        title = request.query_params.get("title", "").strip()
        if title:
            items = items.filter(title__icontains=title)
        return Response(GalleryItemSerializer(items, many=True, context={"request": request}).data)
    serializer = GalleryItemSerializer(data=request.data, context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "HEAD", "PUT", "PATCH", "DELETE"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsPortfolioOwnerOrEditorOrReadOnly])
def gallery_detail(request, item_id):
    item = get_object_or_404(GalleryItem.objects.prefetch_related("starred_by"), pk=item_id)
    if request.method in ("GET", "HEAD"):
        return Response(GalleryItemSerializer(item, context={"request": request}).data)
    if request.method == "DELETE":
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    serializer = GalleryItemSerializer(item, data=request.data, partial=request.method == "PATCH",
                                      context={"request": request})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def gallery_star(request, item_id):
    item = get_object_or_404(GalleryItem, pk=item_id)
    if item.starred_by.filter(pk=request.user.pk).exists():
        item.starred_by.remove(request.user)
    else:
        item.starred_by.add(request.user)
    return Response(GalleryItemSerializer(item, context={"request": request}).data)
