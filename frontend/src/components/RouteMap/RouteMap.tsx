import React, {useState } from 'react';
import {
    YMap,
    YMapComponentsProvider,
    YMapControls,
    YMapDefaultFeaturesLayer,
    YMapDefaultSchemeLayer,
    YMapGeolocationControl,
    YMapListener,
    YMapZoomControl,
} from "ymap3-components";

import { location as LOCATION, apiKey } from './helpers';
import * as YMaps from "@yandex/ymaps3-types";

interface RouteMapProps {
    teamId: number | null
}

const RouteMap: React.FC<RouteMapProps> = ({ teamId }) => {
    const [location, setLocation] = useState(LOCATION);
    const [ymap, setYmap] = useState<YMaps.YMap>();

    const onUpdate = React.useCallback(({ location, mapInAction }: any) => {
        if (!mapInAction) {
            setLocation({
                center: location.center,
                zoom: location.zoom,
            });
        }
    }, []);

    return (
        <div className="w-full h-[42rem]">
            <YMapComponentsProvider apiKey={apiKey} lang='ru_RU'>
                <YMap
                    key="map"
                    ref={(ymap: YMaps.YMap) => setYmap(ymap)}
                    location={location}
                    mode="vector"
                    theme="dark"
                >
                    <YMapDefaultSchemeLayer />
                    <YMapDefaultFeaturesLayer />
                    <YMapListener onUpdate={onUpdate} />
                    <YMapControls position="bottom">
                        <YMapZoomControl />
                    </YMapControls>
                    <YMapControls position="bottom left">
                        <YMapGeolocationControl />
                    </YMapControls>
                </YMap>
            </YMapComponentsProvider>
        </div>
    );
};

export default RouteMap;