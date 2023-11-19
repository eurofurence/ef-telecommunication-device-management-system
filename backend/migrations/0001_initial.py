# Generated by Django 4.2.5 on 2023-09-17 16:40

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('ef_reg_id', models.PositiveIntegerField(help_text='ID of the user in the EF reg database', null=True, unique=True)),
                ('ef_security_collar_id', models.PositiveIntegerField(blank=True, default=None, help_text='ID of the user in the EF security collar database', null=True, unique=True)),
                ('last_seen', models.DateTimeField(blank=True, default=None, help_text='Last time the user was seen on the platform', null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notes', models.CharField(blank=True, default=None, help_text='Optional notes about the item', max_length=512, null=True)),
                ('serialnumber', models.CharField(blank=True, default=None, help_text='Optional serial number of the item', max_length=128, null=True)),
                ('handed_out', models.BooleanField(default=False, help_text='Whether the item is currently handed out')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the item was created')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='Date and time when the item was last updated')),
                ('created_by', models.ForeignKey(blank=True, help_text='User that created the item', null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('polymorphic_ctype', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_%(app_label)s.%(class)s_set+', to='contenttypes.contenttype')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
        ),
        migrations.CreateModel(
            name='ItemOwner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the owner', max_length=128)),
                ('shortname', models.CharField(help_text='Short name of the owner', max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='ItemTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the item this template is for', max_length=128)),
                ('description', models.CharField(blank=True, default=None, help_text='Description of the item this template is for', max_length=256, null=True)),
                ('owner', models.ForeignKey(help_text='User that owns the items that use this template', on_delete=django.db.models.deletion.PROTECT, to='backend.itemowner')),
            ],
        ),
        migrations.CreateModel(
            name='Phone',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.item')),
                ('extension', models.CharField(help_text='Extension (e.g., call number) of the phone', max_length=32)),
                ('dhcp', models.BooleanField(help_text='Whether the phone uses DHCP')),
                ('ip_address', models.GenericIPAddressField(blank=True, help_text='IP address of the phone, if static', null=True)),
                ('mac_address', models.CharField(blank=True, help_text='MAC address of the phone', max_length=17, null=True)),
                ('location', models.CharField(blank=True, help_text='Location of the phone', max_length=128, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('backend.item',),
        ),
        migrations.CreateModel(
            name='PhoneTemplate',
            fields=[
                ('itemtemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.itemtemplate')),
                ('network', models.CharField(choices=[('STAFF', 'Staff'), ('SECU', 'Security')], help_text='Network the phone is on', max_length=8)),
            ],
            bases=('backend.itemtemplate',),
        ),
        migrations.CreateModel(
            name='RadioAccessory',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.item')),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('backend.item',),
        ),
        migrations.CreateModel(
            name='RadioAccessoryTemplate',
            fields=[
                ('itemtemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.itemtemplate')),
                ('allow_quickadd', models.BooleanField(help_text='Whether to allow quick-adding accessories of this type')),
            ],
            bases=('backend.itemtemplate',),
        ),
        migrations.CreateModel(
            name='RadioDevice',
            fields=[
                ('item_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.item')),
                ('callsign', models.CharField(blank=True, help_text='Callsign of the radio', max_length=32, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('backend.item',),
        ),
        migrations.CreateModel(
            name='RadioDeviceTemplate',
            fields=[
                ('itemtemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.itemtemplate')),
            ],
            bases=('backend.itemtemplate',),
        ),
        migrations.CreateModel(
            name='ItemBinding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bound_at', models.DateTimeField(auto_now_add=True, help_text='Date and time when the item was bound')),
                ('bound_by', models.ForeignKey(help_text='User that bound the item', on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('item', models.ForeignKey(help_text='Item that is bound', on_delete=django.db.models.deletion.PROTECT, to='backend.item')),
                ('user', models.ForeignKey(help_text='User that the item is bound to', on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='template',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='backend.itemtemplate'),
        ),
        migrations.CreateModel(
            name='EventLogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now=True, help_text='Timestamp of the event')),
                ('action', models.CharField(choices=[('USER_LOGIN', 'User logged in')], help_text='Action that was performed', max_length=64)),
                ('data', models.JSONField(blank=True, default=None, help_text='Additional data optionally associated with the event', null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Callbox',
            fields=[
                ('phone_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.phone')),
                ('has_camera', models.BooleanField(default=True, help_text='Whether the callbox has a camera')),
                ('camera_ip_address', models.GenericIPAddressField(blank=True, help_text='IP address of the camera', null=True)),
                ('camera_mac_address', models.CharField(blank=True, help_text='MAC address of the camera', max_length=17, null=True)),
            ],
            options={
                'abstract': False,
                'base_manager_name': 'objects',
            },
            bases=('backend.phone',),
        ),
        migrations.CreateModel(
            name='CallboxTemplate',
            fields=[
                ('phonetemplate_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='backend.phonetemplate')),
            ],
            bases=('backend.phonetemplate',),
        ),
    ]
