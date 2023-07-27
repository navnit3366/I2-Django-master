from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Animal, Billet, Equipement
from .forms import MoveForm

def post_list(request):
    billets = Billet.objects.order_by('published_date')
    return render(request, 'animalerie/post_list.html', {'billets': billets})

def animal_list(request):
    animals = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'animalerie/animal_list.html', {'animals': animals,'equipements': equipements})

def equipement_list(request):
    equipements = Equipement.objects.all()
    return render(request, 'animalerie/animal_list.html', {'equipements': equipements})

def post_new(request):
    form = MoveForm()
    return render(request, 'animalerie/post_edit.html', {'form': form})

def animal_detail(request, id_animal,error=None):
    animal = get_object_or_404(Animal, id_animal=id_animal)
    if request.method == "POST":
        form = MoveForm(request.POST)
        if form.is_valid():
            ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
            post = form.save(commit=False)
            nouveau_lieu = get_object_or_404(Equipement, id_equip=post.lieu)
            modif = get_object_or_404(Animal, id_animal=id_animal).changeLieu(nouveau_lieu)
            if modif=='error_not_empty' :
                return redirect('animal_detail_mes', id_animal=id_animal, error='Lieu Occupé')
            elif modif.split(':')[0]=='error_impossible':
                return redirect('animal_detail_mes', id_animal=id_animal, error='Impossible, '+modif.split(':')[1])
            else:
                ancien_lieu.disponibilite = 'libre'
                ancien_lieu.save()
                modif.save()
                nouveau_lieu.disponibilite = 'occupe'
                nouveau_lieu.save()
            return redirect('animal_detail', id_animal=id_animal)
    else:
         form = MoveForm()
    lieu = animal.lieu
    if error==None:
        return render(request,
                    'animalerie/animal_detail.html',
                    {'animal': animal, 'lieu': lieu, 'form': form})
    else:
        return render(request,
                    'animalerie/animal_detail.html',
                    {'animal': animal, 'lieu': lieu, 'form': form, 'error':error})




    # if form.is_valid():
    #     print('VALID !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #     ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    #     ancien_lieu.disponibilite = "libre"
    #     print(ancien_lieu+'a ete libere !!')
    #     ancien_lieu.save(commit=False)
    #     form.save(commit=False)
    #     nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu.id_equip)
    #     nouveau_lieu.disponibilite = "occupe"
    #     nouveau_lieu.save()
    #     animal.lieu = nouveau_lieu
    #     animal.save(commit=False)
    #     return redirect('animal_detail', id_animal=id_animal)
    # else:
    #     print('INVALID !!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    #     lieu=animal.lieu
    #     form = MoveForm()
    #     return render(request,
    #               'animalerie/animal_detail.html',
    #               {'animal': animal, 'lieu': lieu, 'form': form})