import {
  require_react_dom
} from "./chunk-YBFRUR3B.js";
import {
  __toESM,
  require_react
} from "./chunk-JRE55LYH.js";

// node_modules/ymap3-components/dist/index.mjs
var import_react = __toESM(require_react(), 1);
var import_react_dom = __toESM(require_react_dom(), 1);
var f = (0, import_react.createContext)({});
var D = typeof document < "u" ? import_react.useLayoutEffect : import_react.useEffect;
function o(e, c) {
  let a;
  const l = ({ ...t }, p) => {
    const { reactify: s, ymaps: n } = (0, import_react.useContext)(
      f
    ), [M, u] = (0, import_react.useState)(false);
    return D(() => {
      c ? window[c] ? (u(true), a = s.module(window[c])[e]) : n.import(c).then((m) => {
        window[c] = m, s.module(m) && (u(true), a = s.module(m)[e]);
      }) : (a = s.module(n)[e], u(true));
    }, []), !a || !M ? null : import_react.default.createElement(a, { ref: p, ...t });
  };
  return import_react.default.forwardRef(l);
}
var S = async (e, c = "ru_RU") => new Promise(async (a, l) => {
  try {
    if (window.ymaps3) {
      const t = window.ymaps3;
      await t.ready;
      const s = (await t.import("@yandex/ymaps3-reactify")).reactify.bindTo(import_react.default, import_react_dom.default), { YMap: n } = s.module(t);
      a({
        ymaps: t,
        reactify: s
      });
    } else {
      const t = document.createElement("script");
      document.body.appendChild(t), t.type = "text/javascript", t.src = `https://api-maps.yandex.ru/v3/?apikey=${e}&lang=${c}`, t.onload = async () => {
        const p = window.ymaps3;
        await p.ready;
        const n = (await p.import("@yandex/ymaps3-reactify")).reactify.bindTo(import_react.default, import_react_dom.default);
        a({
          ymaps: p,
          reactify: n
        });
      }, t.onerror = l;
    }
  } catch {
  }
});
var v = ({
  apiKey: e,
  lang: c,
  children: a,
  onLoad: l,
  onError: t
}) => {
  const [p, s] = (0, import_react.useState)();
  return D(() => {
    S(e, c).then((n) => {
      s(n), l == null || l(n);
    }).catch((n) => {
      t == null || t(n);
    });
  }, []), p ? import_react.default.createElement(f.Provider, { value: p }, a) : import_react.default.createElement(import_react.default.Fragment, null);
};
var T = import_react.default.memo(v);
var i = ((e) => (e.CartesianProjection = "@yandex/ymaps3-cartesian-projection@0.0.1", e.Clusterer = "@yandex/ymaps3-clusterer@0.0.1", e.Controls = "@yandex/ymaps3-controls@0.0.1", e.Hint = "@yandex/ymaps3-hint@0.0.1", e.Markers = "@yandex/ymaps3-markers@0.0.1", e.SphericalMercatorProjection = "@yandex/ymaps3-spherical-mercator-projection@0.0.1", e))(i || {});
var E = (0, import_react.createContext)({
  hint: void 0
});
var F = ({
  children: e,
  context: c
}) => {
  const a = (0, import_react.useContext)(c);
  return import_react.default.createElement(E.Provider, { value: a }, e);
};
var j = ({ children: e, hint: c }) => {
  const { reactify: a, ymaps: l } = (0, import_react.useContext)(
    f
  ), [t, p] = (0, import_react.useState)(), s = (0, import_react.useMemo)(() => {
    if (t) {
      const n = window[i.Hint];
      return a.module(n).YMapHint;
    }
  }, [t]);
  return (0, import_react.useEffect)(() => {
    if (window[i.Hint]) {
      const n = window[i.Hint];
      p(a.module(n).YMapHintContext);
    } else
      l.import(i.Hint).then((n) => {
        window[i.Hint] = n, a.module(n) && p(a.module(n).YMapHintContext);
      });
  }, []), !s || !t || !e ? import_react.default.createElement(import_react.default.Fragment, null) : import_react.default.createElement(s, { hint: c }, import_react.default.createElement(F, { context: t }, e));
};
var b = import_react.default.forwardRef(({ gridSize: e, method: c, ...a }, l) => {
  const { reactify: t, ymaps: p } = (0, import_react.useContext)(
    f
  ), [s, n] = (0, import_react.useState)(), [M, u] = (0, import_react.useMemo)(() => {
    if (s) {
      const y = window[i.Clusterer];
      return [t.module(y).YMapClusterer, c || t.module(y).clusterByGrid];
    }
    return [];
  }, [s]);
  (0, import_react.useEffect)(() => {
    window[i.Clusterer] ? n(window[i.Clusterer]) : p.import(i.Clusterer).then((y) => {
      window[i.Clusterer] = y, n(y);
    });
  }, []);
  const m = (0, import_react.useMemo)(() => {
    if (u && e)
      return u({ gridSize: e });
  }, [u, e]);
  return !M || !m ? import_react.default.createElement(import_react.default.Fragment, null) : import_react.default.createElement(
    M,
    {
      ref: l,
      method: m,
      ...a
    }
  );
});
var B = o("YMapGeolocationControl", i.Controls);
var G = o("YMapZoomControl", i.Controls);
var $ = o("YMapClusterer", i.Clusterer);
var I = o("YMapDefaultMarker", i.Markers);
var W = o("YMap");
var Z = o("YMapTileDataSource");
var O = o("ThemeContext");
var U = o("YMapControl");
var _ = o("YMapLayer");
var q = o("YMapMarker");
var A = o("YMapDefaultSchemeLayer");
var J = o("YMapDefaultFeaturesLayer");
var K = o("YMapDefaultSatelliteLayer");
var Q = o("YMapListener");
var V = o("YMapControls");
var X = o("YMapControlButton");
var k = o("YMapContainer");
var z = o("YMapCollection");
var P = o("YMapFeature");
var N = o("YMapFeatureDataSource");
export {
  O as ThemeContext,
  W as YMap,
  $ as YMapClusterer,
  z as YMapCollection,
  T as YMapComponentsProvider,
  k as YMapContainer,
  U as YMapControl,
  X as YMapControlButton,
  V as YMapControls,
  b as YMapCustomClusterer,
  J as YMapDefaultFeaturesLayer,
  I as YMapDefaultMarker,
  K as YMapDefaultSatelliteLayer,
  A as YMapDefaultSchemeLayer,
  P as YMapFeature,
  N as YMapFeatureDataSource,
  B as YMapGeolocationControl,
  j as YMapHint,
  E as YMapHintContext,
  _ as YMapLayer,
  Q as YMapListener,
  q as YMapMarker,
  Z as YMapTileDataSource,
  G as YMapZoomControl
};
//# sourceMappingURL=ymap3-components.js.map
