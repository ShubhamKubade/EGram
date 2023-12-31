import smtplib
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import *
from django.db.models import Max
# from .forms import
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from email.message import EmailMessage
import pywhatkit
from .forms import companyforms
from datetime import datetime

from django.http import HttpResponse
from django.http import Http404

def home1(request):
    if request.method == "POST":
        receiver = request.POST["subscriber"]
        print(receiver)
        sender = "myGram"
        subject = "Subscribed to myGram"
        content = "Hello! You have successfully subscribed to myGram"
        sendmail(subject, sender, receiver, content)

    return render(request, 'gramapp/home1.html')


def handlelogin(request):
    if request.method == "POST":
        loginemail = request.POST['loginemail']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginemail, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, '''You Have Successfully Logged In..''')
            return redirect('home1')
        else:
            messages.error(request, '''Incorrect Email or Password..''')
            return redirect('home1')
    return HttpResponse('404')


def handlelogout(request):
    logout(request)
    messages.success(request, '''You Have Successfully Logged Out..''')
    return redirect('home1')


def sendmail(subject, sender, receiver, content):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = receiver
    msg.set_content(content)
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login("miniprojectsecomp@gmail.com", "yptkvurskgdnrpiv")
    server.send_message(msg)
    server.quit()


def whatsappmessage(mobno,message):
    mobno= mobno
    message= message
    pywhatkit.sendwhatmsg_instantly("+91" + mobno, message)


def subscribe(request):
    receiver = request.POST["email"]
    print(receiver)
    # sender = "myGram"
    # subject = "Subscribed to myGram"
    # content = "Hello! You have successfully subscribed to myGram"
    # sendmail(subject, sender, receiver, content)
    return None


def addgram(request):
    current_user = request.user
    if current_user.is_superuser:
        gramid = 1001 if Grampanchayat.objects.count() == 0 else Grampanchayat.objects.aggregate(max=Max('gramid'))[
                                                                     "max"] + 1
        if request.method == "POST":
            gramname = request.POST['gramname']
            gramaddress = request.POST['gramaddress']
            gramemail = request.POST['gramemail']
            gramcontact = request.POST['gramcontact']

            ins = Grampanchayat.objects.create(gramid=gramid, gramname=gramname, gramaddress=gramaddress,
                                               gramemail=gramemail, gramcontact=gramcontact)
            ins.save()

            messages.success(request, '''Grampanchayat Successfully added...''')
            return redirect('home1')
        else:
            return render(request, 'gramapp/addGrampanchayat.html', locals())
    else:
        return render(request, 'gramapp/pageNotFound.html')


def viewgram(request):
    current_user = request.user
    if current_user.is_superuser:
        grampanchayat = Grampanchayat.objects.all()
        context = {'grampanchayat': grampanchayat}
        return render(request, 'gramapp/viewGrampanchayat.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')


def gramdetail(request, pk):
    current_user = request.user
    if current_user.is_superuser:
        eachGram = Grampanchayat.objects.get(gramid=pk)
        gramAdmin = Gramadmin.objects.all().filter(grampanchayat=eachGram)
        context = {'eachGram': eachGram, 'gramAdmin': gramAdmin}
        return render(request, 'gramapp/viewGramDetails.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')

#
# def updateGrampanchayat(request, pk):
#     eachgrampanchayat = Grampanchayat.objects.get(gramid=pk)
#
#     if request.method == "POST":
#         form = gramforms(request.POST, instance=eachgrampanchayat)
#         if form.is_valid():
#             form.save()
#             messages.success(request, eachgrampanchayat.gramname+''' Successfully updated''')
#             return redirect('viewgram')
#         else:
#             return HttpResponse("Error")
#     else:
#         context = {'eachgrampanchayat': eachgrampanchayat}
#         return render(request, 'gramapp/updateGrampanchayat.html', context)
def updateGrampanchayat(request, pk):
    eachgrampanchayat = Grampanchayat.objects.get(gramid=pk)

    if request.method == "POST":
        form = companyforms(request.POST, instance=eachgrampanchayat)
        if form.is_valid():
            form.save()
            return redirect('viewCompany')
        else:
            messages.error(request, ''' Error ''')
    context = {'eachgrampanchayat': eachgrampanchayat}

    return render(request, 'gramapp/updateGrampanchayat.html', context)


def deletegram(request, pk):
    current_user = request.user
    if current_user.is_superuser:
        gram = Grampanchayat.objects.get(gramid=pk)
        try:
            eachGramAdmin = Gramadmin.objects.get(grampanchayat=gram)

            user = User.objects.all().filter(username=eachGramAdmin.user)
            eachGramAdmin.delete()
            user.delete()
            gram.delete()
        except:
            print("error")
        messages.success(request, '''Grampanchayat Successfully deleted...''')
        return redirect('home1')
    else:
        return render(request, 'gramapp/pageNotFound.html')


def addgramadmin(request, pk):
    current_user = request.user
    if current_user.is_superuser:
        gramadminid = 5001 if Gramadmin.objects.count() == 0 else Gramadmin.objects.aggregate(max=Max('gramadminid'))[
                                                                      "max"] + 1
        eachGram = Grampanchayat.objects.get(gramid=pk)
        if request.method == "POST" and request.FILES['gramadminphoto']:
            gramadminphoto = request.FILES['gramadminphoto']
            fss = FileSystemStorage('media/gramadmin/')
            gramadminfname = request.POST['gramadminfname']
            gramadminlname = request.POST['gramadminlname']
            gramadminmobno = request.POST['gramadminmobno']
            gramadminemail = request.POST['gramadminemail']
            gramadminusername = request.POST['gramadminusername']
            gramadminpass = request.POST['gramadminpass']
            gramadmincnfmpass = request.POST['gramadmincnfmpass']
            if gramadminpass == gramadmincnfmpass:
                myuser = User.objects.create_user(gramadminusername, gramadminemail, gramadminpass, is_staff=True)
                myuser.first_name = (gramadminfname)
                myuser.last_name = (gramadminlname)
                myuser.save()

                ins = Gramadmin.objects.create(user=myuser, grampanchayat=eachGram, gramadminid=gramadminid,
                                               gramadminmobno=gramadminmobno, gramadminphoto=gramadminphoto)
                ins.save()

                # Sending Email
                content = "Hello! \n" + gramadminfname + " " + gramadminlname + "\n This is an auto generated message from myGram \n" \
                                                                                " ""Don't share this with anyone \n" \
                                                                                "Your username is: " + gramadminusername + \
                          "\nPassword is:" + gramadminpass + " \nURL:"
                subject = eachGram.gramname + 'Grampanchayat Admin username and password '
                sender = 'myGram'
                receiver = gramadminemail
                sendmail(subject, sender, receiver, content)

                whatsappmessage(gramadminmobno, content)

                messages.success(request, '''Gramapanchayat admin Successfully added...''')
                return redirect('home1')
            else:
                messages.error(request, '''Password does not match''')
                return redirect('addgramadmin')
        else:
            context = {'eachGram': eachGram}
            return render(request, 'gramapp/addgramadmin.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')


def viewGramAdmin(request, pk):
    current_user = request.user
    if current_user.is_superuser:
        eachGramAdmin = Gramadmin.objects.get(gramadminid=pk)
        eachUser = User.objects.get(username=eachGramAdmin.user)
        print(eachUser)
        context = {'eachGramAdmin': eachGramAdmin, 'eachUser': eachUser}
        return render(request, 'gramapp/viewGramAdmin.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')



def deletegramadmin(request, pk):
    current_user = request.user
    if current_user.is_superuser:
        eachGramAdmin = Gramadmin.objects.get(gramadminid=pk)
        user = User.objects.all().filter(username=eachGramAdmin.user)
        user.delete()
        eachGramAdmin.delete()
        messages.success(request, '''Grampanchayat Admin Successfully deleted...''')
        return redirect('home1')
    else:
        return render(request, 'gramapp/pageNotFound.html')



def addBirthDetails(request):
    current_user = request.user
    if current_user.is_staff:
        childid = 1001 if BirthDetail.objects.count() == 0 else BirthDetail.objects.aggregate(max=Max('childid'))[
                                                                    "max"] + 1
        if request.method == "POST" and request.FILES['birthproof']:
            childname = request.POST['childname']
            gender = request.POST['gender']
            birthdate = request.POST['birthdate']
            fathername = request.POST['fathername']
            mothername = request.POST['mothername']
            birthplace = request.POST['birthplace']
            registeredon = request.POST['registeredon']
            birthproof = request.FILES['birthproof']
            fss = FileSystemStorage('media/birthproof/')

            ins = BirthDetail.objects.create(childid=childid, childname=childname, gender=gender, birthdate=birthdate,
                                             fathername=fathername, mothername=mothername, birthplace=birthplace,
                                             registeredon=registeredon,
                                             birthproof=birthproof)
            ins.save()

            messages.success(request, '''New Child Registration Successfully added...''')
            return render(request, 'gramapp/home1.html')
        else:
            return render(request, 'gramapp/addBirthDetails.html', locals())
    else:
        return render(request, 'gramapp/pageNotFound.html')


def requestBirthCertificate(request):
    if request.method == "POST":
        childname = request.POST['childname']
        birthdate = request.POST['birthdate']
        # birthdate_object = datetime.strptime(birthdate, '%m/%d/%y %H:%M:%S')
        birthdetails = BirthDetail.objects.all()

        for i in birthdetails:
            if(i.childname == childname):
                context = {'birthdetails': i}
                return render(request, 'gramapp/birthCertificate.html', context)
            else:
                return HttpResponse("No")
    else:

        return render(request, 'gramapp/requestBirthCertificate.html')



def addAuthority(request):
    return render(request, 'gramapp/addAuthority.html')

def addComplaint(request):
    return render(request, 'gramapp/addComplaint.html')


def addFamilyHead(request):
    current_user = request.user
    if current_user.is_staff:
        familyheadid = 100001 if FamilyHead.objects.count() == 0 else \
        FamilyHead.objects.aggregate(max=Max('familyheadid'))["max"] + 1
        grampanchayat = Grampanchayat.objects.all()
        if request.method == "POST" and request.FILES['familyheadphoto']:
            current_user = request.user
            if current_user.is_superuser:
                selectedgramid = request.POST['gram']
                gram = Grampanchayat.objects.get(gramid=selectedgramid)
            else:
                gramAdmin = Gramadmin.objects.get(user=current_user)
                adminGram = gramAdmin.grampanchayat
                gram = Grampanchayat.objects.get(gramname=adminGram)

            familyheadphoto = request.FILES['familyheadphoto']
            fss = FileSystemStorage('media/family_head/')
            familyheadfname = request.POST['familyheadfname']
            familyheadlname = request.POST['familyheadlname']
            familyheadgender = request.POST['familyheadgender']
            birthdate = request.POST['birthdate']
            familyheadmobno = request.POST['familyheadmobno']
            familyheademail = request.POST['familyheademail']
            familyheadadharno = request.POST['familyheadadharno']
            familyheadpanno = request.POST['familyheadpanno']
            familyincome = request.POST['familyincome']
            rationcardtype = request.POST['rationcardtype']
            rationcardno = request.POST['rationcardno']

            familyheadusername = request.POST['familyheadusername']
            familyheadpass = request.POST['familyheadpass']
            familyheadcnfmpass = request.POST['familyheadcnfmpass']

            myuser = User.objects.create_user(familyheadusername, familyheademail, familyheadpass)
            myuser.first_name = (familyheadfname)
            myuser.last_name = (familyheadlname)
            myuser.save()

            ins = FamilyHead.objects.create(user=myuser, grampanchayat=gram, familyheadid=familyheadid,
                                            familyheadgender=familyheadgender, birthdate=birthdate,
                                            familyheadmobno=familyheadmobno, familyheadadharno=familyheadadharno,
                                            familyheadpanno=familyheadpanno, familyheadphoto=familyheadphoto,
                                            familyincome=familyincome,
                                            rationcardtype=rationcardtype, rationcardno=rationcardno)
            ins.save()

            # Sending Email
            content = "Hello! \n" + familyheadfname + " " + familyheadlname + "\n This is an auto generated message from myGram \n " \
                                                                              "Don't share this with anyone \n" \
                                                                              "Your username is: " + familyheadusername + \
                      "\nPassword is:" + familyheadpass + \
                      " \nURL:"
            subject = 'Grampanchayat Family Head username and password '
            sender = 'myGram'
            receiver = familyheademail
            sendmail(subject, sender, receiver, content)

            whatsappmessage(familyheadmobno, content)

            messages.success(request, '''Family Head Successfully added...''')
            return redirect('home1')
        else:
            context = {'grampanchayat': grampanchayat}
            return render(request, 'gramapp/addFamilyHead.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')


def addFamilymember(request):
    current_user = request.user
    if current_user.is_staff:
        familymemberid = 100001 if Familymembers.objects.count() == 0 else \
        Familymembers.objects.aggregate(max=Max('familymemberid'))["max"] + 1
        current_user = request.user

        if current_user.is_staff:
            if current_user.is_superuser:
                print("superuser")
            if not current_user.is_superuser:
                gramadmin = Gramadmin.objects.get(user=current_user)
                admingram = gramadmin.grampanchayat
                gram = Grampanchayat.objects.get(gramname=admingram)
                familyheads = FamilyHead.objects.all().filter(grampanchayat=gram)

                if request.method == "POST":
                    familyheadid = request.POST['familyhead']
                    family = FamilyHead.objects.get(familyheadid=familyheadid)
                    familymemberfname = request.POST['familymemberfname']
                    relation = request.POST['relation']
                    familymembergender = request.POST['familymembergender']
                    birthdate = request.POST['birthdate']
                    familyheadadharno = request.POST['familyheadadharno']
                    familymemberphoto = request.FILES['familymemberphoto']
                    fss = FileSystemStorage('media/family_member/')

                    ins = Familymembers.objects.create(grampanchayat=gram, family=family, familymemberid=familymemberid,
                                                       familymembername=familymemberfname, relation=relation,
                                                       gender=familymembergender, birthdate=birthdate,
                                                       aadharnop=familyheadadharno,
                                                       familymemberphoto=familymemberphoto, )
                    ins.save()
                    messages.success(request, '''Family Member Successfully added...''')
                    return redirect('home1')
        else:
            print("no")

        context = {'familyheads': familyheads}
        return render(request, 'gramapp/addFamilymember.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')


def viewFamily(request):
    current_user = request.user
    if current_user.is_staff:
        current_user = request.user
        gramadmin = Gramadmin.objects.get(user=current_user)
        admingram = gramadmin.grampanchayat
        gram = Grampanchayat.objects.get(gramname=admingram)
        familyheads = FamilyHead.objects.all().filter(grampanchayat=gram)
        context = {'familyheads': familyheads}
        return render(request, 'gramapp/viewFamily.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')


def viewFamilyDetails(request, pk):
    current_user = request.user
    if current_user.is_staff:
        familyhead = FamilyHead.objects.get(familyheadid=pk)
        familymembers = Familymembers.objects.all().filter(family=familyhead)
        context = {'familyhead': familyhead, 'familymembers': familymembers}
        return render(request, 'gramapp/viewFamilyDetails.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')


def addHouse(request):
    current_user = request.user
    if current_user.is_staff:
        houseid = 200001 if Houses.objects.count() == 0 else Houses.objects.aggregate(max=Max('houseid'))["max"] + 1
        current_user = request.user
        gramadmin = Gramadmin.objects.get(user=current_user)
        admingram = gramadmin.grampanchayat
        gram = Grampanchayat.objects.get(gramname=admingram)
        familyheads = FamilyHead.objects.all().filter(grampanchayat=gram)

        if request.method == "POST":
            houseno = request.POST['houseno']
            region = request.POST['region']
            subregion = request.POST['subregion']
            housetype = request.POST['housetype']
            housearea = request.POST['housearea']
            familyheadid = request.POST['ownername']
            ownername = FamilyHead.objects.get(familyheadid=familyheadid)
            ins = Houses.objects.create(houseno=houseno, gram=gram, houseid=houseid, region=region, subregion=subregion,
                                        housetype=housetype, housearea=housearea,
                                        ownername=ownername)
            ins.save()
            messages.success(request, '''House Successfully added...''')
            return redirect('home1')
        else:
            context = {'familyheads': familyheads}
        return render(request, 'gramapp/addHouse.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')


def viewHouses(request):
    current_user = request.user
    if current_user.is_staff:
        gramadmin = Gramadmin.objects.get(user=current_user)
        admingram = gramadmin.grampanchayat
        houses = Houses.objects.all().filter(gram=admingram)
        context = {'houses': houses}
        return render(request, 'gramapp/viewHouses.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')


def houseDetails(request):
    current_user = request.user
    familyhead = FamilyHead.objects.get(user=current_user)
    houses = Houses.objects.all().filter(ownername=familyhead)
    context = {'houses': houses}

    return render(request, 'gramapp/viewHouseDetails.html', context)


def addHousetax(request):
    current_user = request.user
    if current_user.is_staff:
        housetypeid = 201 if Housetax.objects.count() == 0 else Housetax.objects.aggregate(max=Max('housetypeid'))[
                                                                    "max"] + 1
        if request.method == "POST":
            housetype = request.POST['housetype']
            hosetaxrate = request.POST['hosetaxrate']

            ins = Housetax.objects.create(housetypeid=housetypeid, housetype=housetype, hosetaxrate=hosetaxrate)
            ins.save()
            messages.success(request, '''House Tax Details Successfully added...''')
            return redirect('home1')
        else:
            print("no")
        return render(request, 'gramapp/addHousetax.html')
    else:
        return render(request, 'gramapp/pageNotFound.html')


def viewHouseTax(request, pk):
    house = Houses.objects.get(houseid=pk)
    housetype = house.housetype
    housetax = Housetax.objects.get(housetype=housetype)
    total_housetax = house.housearea * housetax.hosetaxrate
    context = {'house': house, 'housetax': housetax, 'total_housetax': total_housetax}

    return render(request, 'gramapp/viewHouseTax.html', context)


def addWaterConnection(request):
    current_user = request.user
    if current_user.is_staff:
        waterconnectionid = 20001 if WaterConnection.objects.count() == 0 else \
        WaterConnection.objects.aggregate(max=Max('waterconnectionid'))["max"] + 1
        current_user = request.user
        gramadmin = Gramadmin.objects.get(user=current_user)
        admingram = gramadmin.grampanchayat
        gram = Grampanchayat.objects.get(gramname=admingram)
        familyheads = FamilyHead.objects.all().filter(grampanchayat=gram)

        if request.method == "POST":
            waterconnectionno = request.POST['waterconnectionno']
            region = request.POST['region']
            subregion = request.POST['subregion']
            waterconnectiontype = request.POST['waterconnectiontype']
            familyheadid = request.POST['ownername']
            ownername = FamilyHead.objects.get(familyheadid=familyheadid)
            ins = WaterConnection.objects.create(waterconnectionid=waterconnectionid,
                                                 waterconnectionno=waterconnectionno, gram=gram, region=region,
                                                 subregion=subregion,
                                                 waterconnectiontype=waterconnectiontype, ownername=ownername)
            ins.save()
            messages.success(request, '''Water Connection Successfully added...''')
            return redirect('home1')
        else:
            context = {'familyheads': familyheads}
        return render(request, 'gramapp/addWaterConnection.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')


def addWaterTax(request):
    current_user = request.user
    if current_user.is_staff:
        watertaxid = 301 if WaterTax.objects.count() == 0 else WaterTax.objects.aggregate(max=Max('watertaxid'))[
                                                                   "max"] + 1
        if request.method == "POST":
            waterconnectiontype = request.POST['waterconnectiontype']
            watertaxrate = request.POST['watertaxrate']

            ins = WaterTax.objects.create(watertaxid=watertaxid, waterconnectiontype=waterconnectiontype,
                                          watertaxrate=watertaxrate)
            ins.save()
            messages.success(request, '''Water Tax Details Successfully added...''')
            return redirect('home1')
        else:
            print("no")
        return render(request, 'gramapp/addWaterTax.html')
    else:
        return render(request, 'gramapp/pageNotFound.html')


def viewWaterConnections(request):
    current_user = request.user
    if current_user.is_staff:
        gramadmin = Gramadmin.objects.get(user=current_user)
        admingram = gramadmin.grampanchayat
        waterconnections = WaterConnection.objects.all().filter(gram=admingram)
        context = {'waterconnections': waterconnections}
        return render(request, 'gramapp/viewWaterConnections.html', context)
    else:
        return render(request, 'gramapp/pageNotFound.html')


def waterConnectionDetails(request):
    current_user = request.user
    familyhead = FamilyHead.objects.get(user=current_user)
    waterconnections = WaterConnection.objects.all().filter(ownername=familyhead)
    context = {'waterconnections': waterconnections}

    return render(request, 'gramapp/viewWaterConnectionDetails.html', context)


def viewWaterTax(request, pk):
    waterconnection = WaterConnection.objects.get(waterconnectionid=pk)
    waterconnectiontype = waterconnection.waterconnectiontype
    watertax = WaterTax.objects.get(waterconnectiontype=waterconnectiontype)
    total_watertax = watertax.watertaxrate
    context = {'waterconnection': waterconnection, 'waterconnectiontype': waterconnectiontype, 'total_watertax': total_watertax}

    return render(request, 'gramapp/viewWaterTax.html', context)


def addNotice(request):
    noticeid = 3001 if Notice.objects.count() == 0 else Notice.objects.aggregate(max=Max('noticeid'))["max"] + 1
    current_user = request.user
    gramadmin = Gramadmin.objects.get(user=current_user)
    admingram = gramadmin.grampanchayat
    if request.method == "POST":
        gram = Grampanchayat.objects.get(gramname=admingram)
        noticename = request.POST['noticename']
        noticedescription = request.POST['noticedescription']
        noticephoto = request.FILES['noticephoto']
        fss = FileSystemStorage('media/notice/')

        ins = Notice.objects.create(noticeid=noticeid, gram=gram,noticename=noticename,
                                      noticedescription=noticedescription,noticephoto=noticephoto)
        ins.save()
        messages.success(request, '''Notice Successfully added...''')
        return redirect('home1')
    else:
        print("no")

    return render(request, 'gramapp/addNotice.html')


def viewNotice(request):
    current_user = request.user
    familyhead= FamilyHead.objects.get(user=current_user)
    familyheadgram = familyhead.grampanchayat
    gram = Grampanchayat.objects.get(gramname=familyheadgram)

    notices = Notice.objects.all().filter(gram=gram)
    context = {'notices': notices}
    return render(request, 'gramapp/viewNotice.html', context)


def addScheme(request):
    schemeid = 4001 if Scheme.objects.count() == 0 else Scheme.objects.aggregate(max=Max('schemeid'))["max"] + 1
    current_user = request.user
    gramadmin = Gramadmin.objects.get(user=current_user)
    admingram = gramadmin.grampanchayat
    if request.method == "POST":
        gram = Grampanchayat.objects.get(gramname=admingram)
        schemename = request.POST['schemename']
        schemedescription = request.POST['schemedescription']
        schemephoto = request.FILES['schemephoto']
        fss = FileSystemStorage('media/scheme/')

        ins = Scheme.objects.create(schemeid=schemeid, gram=gram,schemename=schemename,
                                      schemedescription=schemedescription,schemephoto=schemephoto)
        ins.save()
        messages.success(request, '''Scheme Successfully added...''')
        return redirect('home1')
    else:
        print("no")

    return render(request, 'gramapp/addScheme.html')


def viewScheme(request):
    current_user = request.user
    familyhead= FamilyHead.objects.get(user=current_user)
    familyheadgram = familyhead.grampanchayat
    gram = Grampanchayat.objects.get(gramname=familyheadgram)

    schemes = Scheme.objects.all().filter(gram=gram)
    context = {'schemes': schemes}
    return render(request, 'gramapp/viewScheme.html', context)

def applyScheme(request, pk):
    return render(request,'gramapp/applyScheme.html')