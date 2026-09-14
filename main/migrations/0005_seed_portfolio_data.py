# Generated manually — seeds production data from local dataset (cleaned)

from django.db import migrations


def seed_data(apps, schema_editor):
    Experience = apps.get_model('main', 'Experience')
    Highlight = apps.get_model('main', 'Highlight')
    GalleryItem = apps.get_model('main', 'GalleryItem')

    experiences = [
        {
            'title': 'VPIC Of Public Relations',
            'description': 'Vice Person in Charge of Public Relations Division.',
            'category': 'full-time',
            'thumbnail': '/static/img/openhouse.png',
        },
        {
            'title': 'Member of Product & Project Management',
            'description': 'Member of Product and Project Management RISTEK Fasilkom UI.',
            'category': 'full-time',
            'thumbnail': '/static/img/ristek.png',
        },
        {
            'title': 'Awardee of Beasiswa Unggulan',
            'description': 'Awardee of Beasiswa Unggulan from Kemendikbud.',
            'category': 'full-time',
            'thumbnail': '/static/img/bu.png',
        },
    ]
    for data in experiences:
        title = data.pop('title')
        Experience.objects.update_or_create(title=title, defaults=data)

    highlights = [
        {
            'title': '5-Day Exchange Program University of Malaya',
            'description': 'Academic exchange program at the University of Malaya.',
            'category': 'Academic Exchange',
            'year': 2026,
            'thumbnail': '/static/img/exchange-um.png',
        },
        {
            'title': 'Semifinalist BPC UISP 2025',
            'description': 'Product: Bring.In',
            'category': 'Business Case Competition',
            'year': 2025,
            'thumbnail': '/static/img/bpc-uisp.jpg',
        },
        {
            'title': '3rd Winner Pekan RISTEK 2025',
            'description': 'Third winner of the Pekan RISTEK mini case competition.',
            'category': 'Mini Case Competition',
            'year': 2025,
            'thumbnail': '/static/img/pekan-ristek.jpg',
        },
        {
            'title': 'Semifinalist BPC EPIC 11th',
            'description': 'Product: Bring.In',
            'category': 'Business Case Competition',
            'year': 2025,
            'thumbnail': '/static/img/bpc-epic.jpg',
        },
    ]
    for data in highlights:
        title = data.pop('title')
        Highlight.objects.update_or_create(title=title, defaults=data)

    gallery_items = [
        {
            'title': 'Kawah Ratu',
            'caption': 'A hike through the Kawah Ratu trail.',
            'category': 'Adventure',
            'location': 'Gunung Salak, Jawa Barat',
            'year': 2025,
            'image': '/static/img/kawah-ratu.jpeg',
            'featured': True,
        },
        {
            'title': 'Gallery UM',
            'caption': 'Academic exchange moments at the University of Malaya.',
            'category': 'Academic Exchange',
            'location': 'University of Malaya',
            'year': 2026,
            'image': '/static/img/gallery-um.jpeg',
            'featured': False,
        },
        {
            'title': 'Raja Padel',
            'caption': 'Alias saya jago banget main padel.',
            'category': 'Sports',
            'location': 'Raja Padel',
            'year': 2026,
            'image': '/static/img/raja-padel.jpeg',
            'featured': True,
        },
        {
            'title': 'Bandung dan Cilembeu',
            'caption': 'Perjalanan ke Bandung dan Cilembeu.',
            'category': 'Travel',
            'location': 'Bandung dan Cilembeu, Jawa Barat',
            'year': 2026,
            'image': '/static/img/cilembeu.jpeg',
            'featured': False,
        },
        {
            'title': 'Bangkok Bersama Keluarga',
            'caption': 'Liburan bersama keluarga di Bangkok.',
            'category': 'Family Trip',
            'location': 'Bangkok, Thailand',
            'year': 2026,
            'image': '/static/img/bangkok.jpeg',
            'featured': False,
        },
    ]
    for data in gallery_items:
        title = data.pop('title')
        GalleryItem.objects.update_or_create(title=title, defaults=data)


def unseed_data(apps, schema_editor):
    Experience = apps.get_model('main', 'Experience')
    Highlight = apps.get_model('main', 'Highlight')
    GalleryItem = apps.get_model('main', 'GalleryItem')

    experience_titles = [
        'VPIC Of Public Relations',
        'Member of Product & Project Management',
        'Awardee of Beasiswa Unggulan',
    ]
    highlight_titles = [
        '5-Day Exchange Program University of Malaya',
        'Semifinalist BPC UISP 2025',
        '3rd Winner Pekan RISTEK 2025',
        'Semifinalist BPC EPIC 11th',
    ]
    gallery_titles = [
        'Kawah Ratu',
        'Gallery UM',
        'Raja Padel',
        'Bandung dan Cilembeu',
        'Bangkok Bersama Keluarga',
    ]

    Experience.objects.filter(title__in=experience_titles).delete()
    Highlight.objects.filter(title__in=highlight_titles).delete()
    GalleryItem.objects.filter(title__in=gallery_titles).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_highlight_thumbnail'),
    ]

    operations = [
        migrations.RunPython(seed_data, unseed_data),
    ]