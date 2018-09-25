# taiga-contrib-fan

Add your favorite projects in the dashbord.

## Installation

```bash
cd /home/taiga
mkdir contrib
cd contrib
git clone https://github.com/leblanc-simon/taiga-contrib-fan.git
```

### Back

```bash
cd /home/taiga/contrib/taiga-contrib-fan/back/taiga_contrib_fan
workon taiga
pip install -e .
```

Edit your `/home/taiga/taiga-back/settings/local.py` and add :

```python
INSTALLED_APPS += ["taiga_contrib_fan"]
```

### Front

```bash
cd /home/taiga/contrib/taiga-contrib-fan/front/taiga-contrib-fan
npm install
gulp build
cd /home/taiga/taiga-front-dist/dist/
mkdir plugins
cd plugins
ln -s /home/taiga/contrib/taiga-contrib-fan/front/taiga-contrib-fan/dist taiga-contrib-fan
```

Edit your `/home/taiga/taiga-front-dist/dist/conf.json` and add :

```js
contribPlugins = [
    "/plugins/taiga-contrib-fan/taiga-contrib-fan.json"
]
```