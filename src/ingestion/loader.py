class Portfolio:
    def __init__(self, name: str, assets: list):
        self.name = name
        self.assets = assets

    def add_asset(self, asset):
        self.assets.append(asset)

    def remove_asset(self, asset):
        self.assets.remove(asset)

    def get_assets(self):
        return self.assets
