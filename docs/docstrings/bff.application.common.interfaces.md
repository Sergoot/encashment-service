<!-- markdownlint-disable -->

<a href="https://github.com/Sergoot/encashment-service/blob/master/bff/bff/application/common/interfaces.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `bff.application.common.interfaces`






---

<a href="https://github.com/Sergoot/encashment-service/blob/master/bff/bff/application/common/interfaces.py#L8"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `ApiClient`







---

<a href="https://github.com/Sergoot/encashment-service/blob/master/bff/bff/application/common/interfaces.py#L9"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get`

```python
get(url: str, query_data: dict | None = None) → dict | list
```





---

<a href="https://github.com/Sergoot/encashment-service/blob/master/bff/bff/application/common/interfaces.py#L15"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `patch`

```python
patch(url: str, data: dict) → dict
```





---

<a href="https://github.com/Sergoot/encashment-service/blob/master/bff/bff/application/common/interfaces.py#L12"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `post`

```python
post(url: str, data: dict) → dict
```






---

<a href="https://github.com/Sergoot/encashment-service/blob/master/bff/bff/application/common/interfaces.py#L19"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `RouteResponse`
RouteResponse(next_step: Any) 

<a href="https://github.com/Sergoot/encashment-service/blob/master/<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(next_step: Any) → None
```









---

<a href="https://github.com/Sergoot/encashment-service/blob/master/bff/bff/application/common/interfaces.py#L24"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `IComputeRoute`







---

<a href="https://github.com/Sergoot/encashment-service/blob/master/bff/bff/application/common/interfaces.py#L25"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `execute`

```python
execute(command: ComputeRouteCommand) → RouteResponse
```








---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
