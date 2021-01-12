# itinehari

Python cli itinerary tool based on citymapper api

## Usage

```bash
$ hari le peletier - bourg la reine
```

```text
- Total: 39 min - ETA: 11:44
├── Walk - 2 min
├── M8 - 2 min
│   ├── Richelieu - Drouot 11:10
│   └── Madeleine 11:12
├── Walk - 1 min
├── M14 - 4 min
│   ├── Madeleine 11:15
│   └── Châtelet 11:19
├── Walk - 3 min
├── RER B - 15 min
│   ├── Châtelet - Les Halles 11:23
│   └── Bourg-la-Reine 11:38
└── Walk - 6 min
https://citymapper.com/directions?start=48.871951%2C2.338082&end=48.780114%2C2.316521&region_id=fr-paris
```

## Note

It also supports standard input/output like:

`echo 12 rue faubourg du temple - 7 rue des templiers | hari >> itineraries`
