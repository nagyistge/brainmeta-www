from django.test import TestCase, Client
from neurovault.apps.statmaps.models import Collection,User, StatisticMap
import os
from django.core.files.uploadedfile import SimpleUploadedFile
from neurovault.apps.statmaps.forms import StatisticMapForm
from .utils import clearDB

class AddStatmapsTests(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user('NeuroGuy')
        self.user.save()
        self.client = Client()
        self.client.login(username=self.user)
        self.coll = Collection(owner=self.user, name="Test Collection")
        self.coll.save()
        
    def tearDown(self):
        clearDB()

    def testaddNiiGz(self):

            post_dict = {
                'name': "test map",
                'cognitive_paradigm_cogatlas': 'trm_4f24126c22011',
                'modality':'fMRI-BOLD',
                'map_type': 'T',
                'collection':self.coll.pk,
            }
            testpath = os.path.abspath(os.path.dirname(__file__))
            fname = os.path.join(testpath,'test_data/statmaps/motor_lips.nii.gz')
            file_dict = {'file': SimpleUploadedFile(fname, open(fname).read())}
            form = StatisticMapForm(post_dict, file_dict)

            self.assertTrue(form.is_valid())

            form.save()
            
            self.assertEqual(StatisticMap.objects.filter(collection=self.coll.pk)[0].name, "test map")
            
    def testaddImgHdr(self):

            post_dict = {
                'name': "test map",
                'cognitive_paradigm_cogatlas': 'trm_4f24126c22011',
                'modality':'fMRI-BOLD',
                'map_type': 'T',
                'collection':self.coll.pk,
            }
            testpath = os.path.abspath(os.path.dirname(__file__))
            fname_img = os.path.join(testpath,'test_data/statmaps/box_0b_vs_1b.img')
            fname_hdr = os.path.join(testpath,'test_data/statmaps/box_0b_vs_1b.hdr')
            file_dict = {'file': SimpleUploadedFile(fname_img, open(fname_img).read()),
                         'hdr_file': SimpleUploadedFile(fname_hdr, open(fname_hdr).read())}
            form = StatisticMapForm(post_dict, file_dict)
            self.assertFalse(form.is_valid())
            self.assertTrue("thresholded" in form.errors["file"][0])
            
            post_dict = {
                'name': "test map",
                'cognitive_paradigm_cogatlas': 'trm_4f24126c22011',
                'modality':'fMRI-BOLD',
                'map_type': 'T',
                'collection':self.coll.pk,
                'ignore_file_warning': True
            }
            testpath = os.path.abspath(os.path.dirname(__file__))
            fname_img = os.path.join(testpath,'test_data/statmaps/box_0b_vs_1b.img')
            fname_hdr = os.path.join(testpath,'test_data/statmaps/box_0b_vs_1b.hdr')
            file_dict = {'file': SimpleUploadedFile(fname_img, open(fname_img).read()),
                         'hdr_file': SimpleUploadedFile(fname_hdr, open(fname_hdr).read())}
            form = StatisticMapForm(post_dict, file_dict)
            self.assertTrue(form.is_valid())

            form.save()
            
            self.assertEqual(StatisticMap.objects.filter(collection=self.coll.pk)[0].name, "test map")