# Simulatie protocool

Om de simulatie met de server te laten communiceren is het volgende protocool opgesteld. In dit protocool staan alle commando's beschreven die gegeven kunnen worden en de reacties die daarop kunnen worden verwacht.

## Commando's

### Ophalen van de software drones
#### Commando
Om alle software drones op te vragen moet het volgende command worden gestuurd:
```json
{
    "command": "getSoftwareDrones"
}
```

#### Reacties
De volgende reacties kunnen worden verwacht.

##### Drones
Er zal een lijst met drones worden terugegeven die er als volgt uit kan zien:
```json
[
    {
        "droneId": "1",
        "master": true,
        "batteryVoltage": 0,
        "isCharging": false,
        "isFlying": true,
        "isTumbled": false,
        "locationX": 105,
        "locationY": 208,
        "locationZ": 30,
        "direction": 80,
        "distanceDown": 300,
        "distanceFront": 60,
        "distanceBack": 463,
        "distanceLeft": 287,
        "distanceRight": 189,
        "ldr": 1.3,
        "ldrMax": 1.5,
        "colorFront": "#00FF00",
        "colorBack": "#FF0000"
    },
    {
        "droneId": "2",
        "master": false,
        "batteryVoltage": 0,
        "isCharging": false,
        "isFlying": false,
        "isTumbled": false,
        "locationX": 876,
        "locationY": 348,
        "locationZ": 30,
        "direction": 80,
        "distanceDown": 300,
        "distanceFront": 60,
        "distanceBack": 463,
        "distanceLeft": 287,
        "distanceRight": 189,
        "ldr": 1.2,
        "ldrMax": 1.4,
        "colorFront": "#0000FF",
        "colorBack": "#FF0000"
    }
]
```

### Ophalen van de hardware drones
#### Commando
Om alle hardware drones op te vragen moet het volgende command worden gestuurd:
```json
{
    "command": "getHardwareDrones"
}
```

#### Reacties
De volgende reacties kunnen worden verwacht.

##### Drones 
Er zal een lijst met drones worden terugegeven die er als volgt uit kan zien:
```json
[
    {
        "droneId": "1",
        "master": true,
        "batteryVoltage": 0,
        "isCharging": false,
        "isFlying": true,
        "isTumbled": false,
        "locationX": 105,
        "locationY": 208,
        "locationZ": 30,
        "direction": 80,
        "distanceDown": 300,
        "distanceFront": 60,
        "distanceBack": 463,
        "distanceLeft": 287,
        "distanceRight": 189,
        "ldr": 1.3,
        "ldrMax": 1.5,
        "colorFront": "#00FF00",
        "colorBack": "#FF0000"
    },
    {
        "droneId": "2",
        "master": false,
        "batteryVoltage": 0,
        "isCharging": false,
        "isFlying": false,
        "isTumbled": false,
        "locationX": 876,
        "locationY": 348,
        "locationZ": 30,
        "direction": 80,
        "distanceDown": 300,
        "distanceFront": 60,
        "distanceBack": 463,
        "distanceLeft": 287,
        "distanceRight": 189,
        "ldr": 1.2,
        "ldrMax": 1.4,
        "colorFront": "#0000FF",
        "colorBack": "#FF0000"
    }
]
```

### Verbinden van een software drone
#### Commando
Om een software drone te verbinden moet het volgende command worden gestuurd:
```json
{
    "command": "connectSoftwareDrone",
    "droneId": "1"
}
```
Tijdens dit bovenstaande command is het `droneId` het id van de drone die verbonden moet worden.

#### Reacties
De volgende reacties kunnen worden verwacht.

##### Connected
Als de verbinding geslaagd is wordt het volgende teruggestuurd:
```json
{
    "connected": true
}
```

##### Not connecting
Wanneer de server nog geen verbinding wilt maken met de drones dan wordt het volgende terugegestuurd:
```json
{
    "error": "notConnecting"
}
```

##### Ongeldige drone
Wanneer de server de meegegeven drone niet kent zal het volgende worden teruggestuurd:
```json
{
    "error": "invalidDrone"
}
```

### Ophalen van de velocity van een software drone
#### Commando
Om de velocity van een software drone op te vragen moet het volgende command worden gestuurd:
```json
{
    "command": "getSoftwareDroneVelocity",
    "droneId": "1"
}
```
Tijdens dit bovenstaande command is het `droneId` het id van de drone waarvan de velocity opgevraagd moet worden.

#### Reacties
De volgende reacties kunnen worden verwacht.

##### Velocity
Als de drone wordt herkent wordt het volgende teruggestuurd:
```json
{
    "droneId": "1",
    "velocityX": "0.2",
    "velocityY": "0",
    "rate": "10"
}
```

##### Ongeldige drone
Wanneer de server de meegegeven drone niet kent zal het volgende worden teruggestuurd:
```json
{
    "error": "invalidDrone"
}
```

### Data naar de software drone versturen
#### Commando
Om de data van een drone te versturen naar de server moet het volgende command worden gestuurd:
```json
{
    "command": "setSoftwareDrone",
    "droneId": "1",
    "data": {
        "batteryVoltage": "4.1",
        "isCharging": false,
        "isFlying": false,
        "isTumbled": false,
        "locationX": 100,
        "locationY": 50,
        "locationZ": 20,
        "direction": 80,
        "distanceDown": 50,
        "distanceFront": 10,
        "distanceBack": 30,
        "distanceLeft": 300,
        "distanceRight": 500,
        "ldr": 2.3
    }
}
```
Tijdens dit bovenstaande command is het `droneId` het id van de drone waarvan de data moet worden aangepast. Niet alle punten die in het `data` object staan hoeven meegegeven te worden, alleen de data die hierin is meegegegeven wordt aangepast. Zie voorbeeld:
```json
{
    "command": "setSoftwareDrone",
    "droneId": "2",
    "data": {
        "ldr": 1.2
    }
}
```
Bij dit bovenstaande voorbeeld wordt alleen de `ldr` data aangepast.

#### Reacties
De volgende reacties kunnen worden verwacht.

##### Data saved succesfull
Als de drone wordt herkent wordt het volgende teruggestuurd:
```json
{
    "set": true
}
```
##### Ongeldige drone
Wanneer de server de meegegeven drone niet kent zal het volgende worden teruggestuurd:
```json
{
    "error": "invalidDrone"
}
```

##### Ongeldige data
Wanneer de server één van de meeggegeven data punten niet herkent zal het volgende worden teruggestuurd:
```json
{
    "error": "invalidData"
}
```

## Ongeldig commando
Als er een ongeldig commando wordt gestuurd dan wordt het volgende als response teruggestuurd:
```json
{
    "error": "invalidCommand"
}
```