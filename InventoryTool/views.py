from django.shortcuts import render
from django.http import HttpResponse
from pydeck import View


# Create your views here.


def index(request):
        return HttpResponse("Hello, world!")

class ProjectView(View):

    def post(self, request):
        return HttpResponse("Hello, world! post reached")


"""class RegistrationAPIView(generics.GenericAPIView):

    serializer_class = RegistrationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        #serializer.is_valid(raise_exception=True)
        #serializer.save()
        if serializer.is_valid():
            serializer.save()
            return Response({
                "RequestId": str(uuid.uuid4()),
                "Message": "User created successfully!!",

                "user": serializer.data
                },
                status=status.HTTP_201_CREATED
                )

        return Response({"Errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)"""