from rest_framework.decorators  import api_view
from rest_framework.response import Response 
from django.views.decorators.csrf import csrf_exempt
from .utils.stk_push import stk_push

@csrf_exempt
@api_view(['POST'])
def pay_mpesa(request):
    if request.method == 'POST':
        phone_number = request.data['phone_number']
        amount = request.data['amount']
        amount = 1
        stk_push(phone_number, amount)
        response = 'payment initiaited'
        return Response(response)
   
    