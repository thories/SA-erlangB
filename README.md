# Splunk Addon - SA-erlangB
Splunk Supporting Add-on which provides command to use erlangB calculation. 

Example:

```| stats count | eval traffic_field=47.759 | erlang field=traffic_field blocking_factor=0.01 result=trunks```

---

Credits:

* Splunk SDK: https://github.com/splunk/splunk-sdk-python
* Icon: https://www.iconfinder.com/icons/1055102/calculation_calculator_math_mathematics_icon

