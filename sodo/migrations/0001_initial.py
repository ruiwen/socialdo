# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):
    
    def forwards(self, orm):
        
        # Adding model 'User'
        db.create_table('sodo_user', (
            ('user_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True, primary_key=True)),
            ('profile_image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
        ))
        db.send_create_signal('sodo', ['User'])

        # Adding M2M table for field contacts on 'User'
        db.create_table('sodo_user_contacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_user', models.ForeignKey(orm['sodo.user'], null=False)),
            ('to_user', models.ForeignKey(orm['sodo.user'], null=False))
        ))
        db.create_unique('sodo_user_contacts', ['from_user_id', 'to_user_id'])

        # Adding model 'List'
        db.create_table('sodo_list', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('date_modified', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('parent_list', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='sub_lists', null=True, to=orm['sodo.List'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(related_name='owned_lists', to=orm['sodo.User'])),
            ('date_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=1024, null=True, blank=True)),
        ))
        db.send_create_signal('sodo', ['List'])

        # Adding M2M table for field collaborators on 'List'
        db.create_table('sodo_list_collaborators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('list', models.ForeignKey(orm['sodo.list'], null=False)),
            ('user', models.ForeignKey(orm['sodo.user'], null=False))
        ))
        db.create_unique('sodo_list_collaborators', ['list_id', 'user_id'])

        # Adding model 'Item'
        db.create_table('sodo_item', (
            ('date_completed', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('primary_list', self.gf('django.db.models.fields.related.ForeignKey')(related_name='primary_items', to=orm['sodo.List'])),
            ('completed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='completed_items', null=True, to=orm['sodo.User'])),
            ('date_modified', self.gf('django.db.models.fields.DateField')(auto_now=True, blank=True)),
            ('completed', self.gf('django.db.models.fields.BooleanField')(default=False, blank=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['sodo.User'])),
            ('date_added', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal('sodo', ['Item'])

        # Adding M2M table for field secondary_lists on 'Item'
        db.create_table('sodo_item_secondary_lists', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('item', models.ForeignKey(orm['sodo.item'], null=False)),
            ('list', models.ForeignKey(orm['sodo.list'], null=False))
        ))
        db.create_unique('sodo_item_secondary_lists', ['item_id', 'list_id'])
    
    
    def backwards(self, orm):
        
        # Deleting model 'User'
        db.delete_table('sodo_user')

        # Removing M2M table for field contacts on 'User'
        db.delete_table('sodo_user_contacts')

        # Deleting model 'List'
        db.delete_table('sodo_list')

        # Removing M2M table for field collaborators on 'List'
        db.delete_table('sodo_list_collaborators')

        # Deleting model 'Item'
        db.delete_table('sodo_item')

        # Removing M2M table for field secondary_lists on 'Item'
        db.delete_table('sodo_item_secondary_lists')
    
    
    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'sodo.item': {
            'Meta': {'object_name': 'Item'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'completed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'completed_items'", 'null': 'True', 'to': "orm['sodo.User']"}),
            'date_added': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_completed': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateField', [], {'auto_now': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'primary_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary_items'", 'to': "orm['sodo.List']"}),
            'secondary_lists': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'secondary_items'", 'symmetrical': 'False', 'to': "orm['sodo.List']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': "orm['sodo.User']"})
        },
        'sodo.list': {
            'Meta': {'object_name': 'List'},
            'collaborators': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'shared_lists'", 'symmetrical': 'False', 'to': "orm['sodo.User']"}),
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '1024', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'owned_lists'", 'to': "orm['sodo.User']"}),
            'parent_list': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'sub_lists'", 'null': 'True', 'to': "orm['sodo.List']"})
        },
        'sodo.user': {
            'Meta': {'object_name': 'User', '_ormbases': ['auth.User']},
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['sodo.User']", 'symmetrical': 'False', 'blank': 'True'}),
            'profile_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }
    
    complete_apps = ['sodo']
