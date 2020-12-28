from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib import messages
from YAMLDatabase.forms import yamlform
from .forms import *
from django.forms import modelformset_factory
import sys
import yaml
from django.db import IntegrityError


# Create your views here.


def index(request,filename_id):
    filename = Filename.objects.get(pk=filename_id)
    YAMLEntryFormset = modelformset_factory(YAMLEntry,fields =('hostname','host','username','password','device_type'))
    if request.method == 'POST':
        try:
            formset = YAMLEntryFormset(request.POST, queryset=YAMLEntry.objects.filter(filename_id=filename.id))
            if formset.is_valid():
                instances = formset.save(commit=False)
                for instance in instances:
                    instance.filename_id = filename.id
                    instance.save()


        except IntegrityError as e:


            return HttpResponse("Hostname already present in the Testbed. Go back and enter a new hostname.")


        result1 = Filename.objects.get(id=filename_id)
        filenumber = result1.id
        filename1 = result1.filename

        YAMLObject = YAMLEntry.objects.all().filter(filename__filename=filename1)

        list1 = []
        length = len(YAMLObject)

        A = []

        for k in range(0, length):
            dict = {}
            dict['hostname'] = YAMLObject[k].hostname
            dict['host'] = YAMLObject[k].host
            dict['username'] = YAMLObject[k].username
            dict['password'] = YAMLObject[k].password
            dict['device_type'] = YAMLObject[k].device_type
            A.append(dict)
        dict1 = {}
        dict1['name'] = filename1
        dict1['hosts'] = A
        dict2 = {}
        dict2['username'] = "root"
        dict2['password'] = "sitlab123!"

        dict3 = {}
        dict3['vars'] = dict2
        dict3['sites'] = dict1

        dict4 = {}
        dict4['all'] = dict3

        with open("{}.yaml".format(filename1), 'w') as file:
            yaml.dump(dict4, file)

        return redirect('index', filename_id = filename.id)
    formset = YAMLEntryFormset(queryset = YAMLEntry.objects.filter(filename_id=filename.id))


    return render(request, 'index.html', {'formset':formset,'filename':filename})



def yamldisplays(request, note_id):
    result1 = Filename.objects.get(id=note_id)
    filenumber=result1.id
    filename1 = result1.filename
    print(filename1)
    print(filenumber)


    YAMLObject = YAMLEntry.objects.all().filter(filename__filename=filename1).order_by('hostname')



    list1 = []
    length = len(YAMLObject)

    A = []

    for k in range(0,length):
        dict = {}
        dict['hostname'] = YAMLObject[k].hostname
        dict['host'] = YAMLObject[k].host
        dict['username'] = YAMLObject[k].username
        dict['password'] = YAMLObject[k].password
        dict['device_type'] = YAMLObject[k].device_type
        A.append(dict)
    dict1 = {}
    dict1['name'] = filename1
    dict1['hosts'] = A
    dict2 = {}
    dict2['username'] = "root"
    dict2['password'] = "sitlab123!"

    dict3 = {}
    dict3['vars'] = dict2
    dict3['sites'] = dict1

    dict4 = {}
    dict4['all'] = dict3

    with open("{}.yaml".format(filename1), 'w') as file:
        yaml.dump(dict4, file)

    print("length",length)

    for i in range(0,length):

        list = []
        list.append(YAMLObject[i].filename)
        list.append(YAMLObject[i].hostname)
        list.append(YAMLObject[i].host)
        list.append(YAMLObject[i].username)
        list.append(YAMLObject[i].password)
        list.append(YAMLObject[i].device_type)
        list.append(YAMLObject[i].id)
        list.append(YAMLObject[i].id)

        list1.append(list)

    print(list1)

    return render(request, "Dashboard.html",{"lists":list1,"length":length,"filenumber":filenumber,"filename":filename1})


def filenamedisplay(request):
    resultsFile = Filename.objects.all().order_by('filename')
    return render(request, "TestBed.html",{"Filename":resultsFile})



def filenameinsert(request):
    if request.method == "POST":
        if request.POST.get('filename'):
            try:
                savefile = Filename()
                savefile.filename = request.POST.get('filename')
                savefile.save()
                #messages.success(request, "Testbed file is created. Go to Add Hosts to add hosts.")
                return redirect(index, filename_id=savefile.id)

            except IntegrityError as e:

                print("Filename already exists!!!")
                message="Filename already exists!!!"
                return render(request, "FilenameEntry.html", {"message":message})


    return render(request, "FilenameEntry.html",{})


def filenamedelete(request,id):
    delfile = Filename.objects.get(id=id)
    delfile.delete()
    results = Filename.objects.all().order_by('filename')
    return render(request,"TestBed.html",{"Filename":results})




def yamledit(request,id):
    getYAMLDetails = YAMLEntry.objects.get(id=id)
    return render(request,'edit.html',{"YAMLEntry":getYAMLDetails})


def yamlupdate(request,id):
    yamlupdate = YAMLEntry.objects.get(id=id)
    fileid = yamlupdate.filename_id
    filename = yamlupdate.filename
    form = yamlform(instance=yamlupdate)

    if request.method == "POST":
        form = yamlform(request.POST,instance = yamlupdate)

        if form.is_valid():
            form.save()
            #messages.success(request, "The host record is updated successfully...!")
            return redirect(yamldisplays, note_id=fileid)


    return render(request, "edit1.html", {"YAMLEntry": form,"filename":filename,"id":id})



def yamldelete1(request,id):

    delyaml = YAMLEntry.objects.get(id=id)
    fileid = delyaml.filename_id
    if request.method == "POST":
        delyaml.delete()
        #messages.success(request, "The host record is deleted successfully...Update .yaml file!")
        return redirect(yamldisplays, note_id=fileid)
    return render(request, "edit.html",{"YAMLEntry":delyaml,"id1":fileid})

