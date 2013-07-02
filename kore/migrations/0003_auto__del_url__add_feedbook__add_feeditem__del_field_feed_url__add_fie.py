# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Url'
        db.delete_table(u'kore_url')

        # Adding model 'FeedBook'
        db.create_table(u'kore_feedbook', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'kore', ['FeedBook'])

        # Adding model 'FeedItem'
        db.create_table(u'kore_feeditem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kore.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('header_img', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('unread', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'kore', ['FeedItem'])

        # Deleting field 'Feed.url'
        db.delete_column(u'kore_feed', 'url_id')

        # Adding field 'Feed.link'
        db.add_column(u'kore_feed', 'link',
                      self.gf('django.db.models.fields.URLField')(default=u'http://google.com', unique=True, max_length=500),
                      keep_default=False)

        # Adding field 'Feed.feed_book'
        db.add_column(u'kore_feed', 'feed_book',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['kore.FeedBook'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Feed.last_sync'
        db.add_column(u'kore_feed', 'last_sync',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 7, 2, 0, 0)),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Url'
        db.create_table(u'kore_url', (
            ('link', self.gf('django.db.models.fields.URLField')(max_length=255, unique=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal(u'kore', ['Url'])

        # Deleting model 'FeedBook'
        db.delete_table(u'kore_feedbook')

        # Deleting model 'FeedItem'
        db.delete_table(u'kore_feeditem')


        # User chose to not deal with backwards NULL issues for 'Feed.url'
        raise RuntimeError("Cannot reverse this migration. 'Feed.url' and its values cannot be restored.")
        # Deleting field 'Feed.link'
        db.delete_column(u'kore_feed', 'link')

        # Deleting field 'Feed.feed_book'
        db.delete_column(u'kore_feed', 'feed_book_id')

        # Deleting field 'Feed.last_sync'
        db.delete_column(u'kore_feed', 'last_sync')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'kore.feed': {
            'Meta': {'object_name': 'Feed'},
            'feed_book': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kore.FeedBook']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_sync': ('django.db.models.fields.DateTimeField', [], {}),
            'link': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '500'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'kore.feedbook': {
            'Meta': {'object_name': 'FeedBook'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'kore.feeditem': {
            'Meta': {'object_name': 'FeedItem'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['kore.Feed']"}),
            'header_img': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'unread': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        }
    }

    complete_apps = ['kore']