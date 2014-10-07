django-site-settings
====================

Use database driven settings for your Django site.

## Installation


### 1. Get

```
pip install django-site-settings
```

Or

```
git clone git@github.com:g3rd/django-site-settings.git
cd django-site-settings
pip install -e .
```

### 2. Add to Django settings.py file

Add to installed apps

```
INSTALLED_APPS += (
    'polymorphic',
    'parler',
    'site_settings',
)
```

## To do

- [ ] Middleware to pull settings for views
- [ ] Template tag and Template Context Processor


## Change Log

| Date | Version | Notes |
|:----:|:-------:|:-----:|
| 2014-Oct. 7 | 20141007.1 | Initial |
