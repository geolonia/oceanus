#!/bin/bash
if [ ! -e /data/110m_physical/110m_physical.zip ]; then
    mkdir /data/110m_physical
    curl -L https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/physical/110m_physical.zip -o /data/110m_physical/110m_physical.zip
    unzip -o /data/110m_physical/110m_physical.zip -d /data/110m_physical
fi
if [ ! -e /data/110m_cultural/110m_cultural.zip ]; then
    mkdir /data/110m_cultural
    curl -L https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/110m/cultural/110m_cultural.zip -o /data/110m_cultural/110m_cultural.zip
    unzip -o /data/110m_cultural/110m_cultural.zip -d /data/110m_cultural
fi
if [ ! -e /data/50m_physical/50m_physical.zip ]; then
    mkdir /data/50m_physical
    curl -L https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/physical/50m_physical.zip -o /data/50m_physical/50m_physical.zip
    unzip -o /data/50m_physical/50m_physical.zip -d /data/50m_physical
fi
if [ ! -e /data/50m_cultural/50m_cultural.zip ]; then
    mkdir /data/50m_cultural
    curl -L https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/50m/cultural/50m_cultural.zip -o /data/50m_cultural/50m_cultural.zip
    unzip -o /data/50m_cultural/50m_cultural.zip -d /data/50m_cultural
fi
if [ ! -e /data/10m_physical/10m_physical.zip ]; then
    mkdir /data/10m_physical
    curl -L https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/physical/10m_physical.zip -o /data/10m_physical/10m_physical.zip
    unzip -o /data/10m_physical/10m_physical.zip -d /data/10m_physical
fi
if [ ! -e /data/10m_cultural/10m_cultural.zip ]; then
    mkdir /data/10m_cultural
    curl -L https://www.naturalearthdata.com/http//www.naturalearthdata.com/download/10m/cultural/10m_cultural.zip -o /data/10m_cultural/10m_cultural.zip
    unzip -o /data/10m_cultural/10m_cultural.zip -d /data/
fi