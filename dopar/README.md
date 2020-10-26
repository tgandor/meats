# dopar

... the would be competition for GNU parallel (just kidding).

For simple cases where there is no benefit to running the jobs for each item at a time:

```
ls <glob_for_stuff_to_process> | xargs -n 200 -P `nproc` command... options... 
```

This is a bit dumb, because you need to specify both the number of CPUs and the batch size (-n).

For N = 5000 there is no real difference between `-n` of 200 and 625 (optimal for `nproc` = 8).

```
ls <glob_for_stuff_to_process> | xargs -n len(<glob_for_stuff_to_process)/`nproc` -P `nproc` command... options... 
```

