<!-- markdownlint-disable -->

# API Overview

## Modules

- [`bff`](./bff.md#module-bff)
- [`bff.adapters`](./bff.adapters.md#module-bffadapters)
- [`bff.application`](./bff.application.md#module-bffapplication)
- [`bff.application.common`](./bff.application.common.md#module-bffapplicationcommon)
- [`bff.application.common.commands`](./bff.application.common.commands.md#module-bffapplicationcommoncommands)
- [`bff.application.common.interfaces`](./bff.application.common.interfaces.md#module-bffapplicationcommoninterfaces)
- [`bff.application.services`](./bff.application.services.md#module-bffapplicationservices)
- [`bff.application.services.compute_route`](./bff.application.services.compute_route.md#module-bffapplicationservicescompute_route)
- [`bff.main`](./bff.main.md#module-bffmain)
- [`bff.presentation`](./bff.presentation.md#module-bffpresentation)
- [`bff.presentation.schemas`](./bff.presentation.schemas.md#module-bffpresentationschemas)
- [`bff.presentation.schemas.requests`](./bff.presentation.schemas.requests.md#module-bffpresentationschemasrequests)
- [`tests`](./tests.md#module-tests)

## Classes

- [`commands.ComputeRouteCommand`](./bff.application.common.commands.md#class-computeroutecommand): ComputeRouteCommand(current_lat: float, current_long: float, radius: int)
- [`interfaces.ApiClient`](./bff.application.common.interfaces.md#class-apiclient)
- [`interfaces.IComputeRoute`](./bff.application.common.interfaces.md#class-icomputeroute)
- [`interfaces.RouteResponse`](./bff.application.common.interfaces.md#class-routeresponse): RouteResponse(next_step: Any)
- [`compute_route.ComputeRoute`](./bff.application.services.compute_route.md#class-computeroute)
- [`requests.ComputeRouteQuery`](./bff.presentation.schemas.requests.md#class-computeroutequery): ComputeRouteQuery(current_lat: float, current_long: float, radius: int = 1000)

## Functions

- No functions


---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
