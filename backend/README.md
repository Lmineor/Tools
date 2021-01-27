### 诗词API

- 获取所有的诗人

```py
url:port/poem/poets
```

- 获取指定诗人的所有诗作

```py
url:port/poem/poems?poet=李白&dynasty=唐
```

注意：

- 若不指定poet或dynasty，则默认返回唐-李白的所有诗作