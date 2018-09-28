import os
from datetime import datetime, timedelta

class LoadRegister:

    def __init__(self, interval, monitortime, error_interval):
        self._dpoints_num = (int) (monitortime/interval);
        self._min_error_dps = (int) (error_interval / interval)
        self._interval = interval
        self._load_stats = []
        self._overload = False
        self._messages = []
        self._uptime = datetime.now()
        self._max = 0
        self._min = 0
        self._avg = 0

    # only adding curload signature for testing purpose
    def add_datapoint(self, curload=None):
        cur_dpnum = len(self._load_stats)
        if cur_dpnum == self._dpoints_num:
            del self._load_stats[0]
        assert len(self._load_stats) < self._dpoints_num
        FMT = '%Y-%m-%d %H:%M:%S'
        curtime = datetime.now()
        curtime_str = curtime.strftime(FMT)
        if not curload:
        	curload = float("{0:5f}".format(os.getloadavg()[0]))
        newItem = {'time':curtime_str, 'load': curload}
        # updating key metrics
        if cur_dpnum ==0:
            self._max = self._min = curload
        else:
            if curload > self._max:
                self._max = curload
            elif curload < self._min:
                self._min = curload
        self._load_stats.append(newItem)
       	self._avg = self._calculate_average()
        self._generate_messages()

    def _calculate_average(self):
        total_load = 0;
        for each in self._load_stats:
            total_load = total_load + each['load']
        return float("{0:5f}".format(total_load / len(self._load_stats)))

    def get_stats(self):
        # if _load_stats has less datapoints than what's good for display, fill them with fake empty points
        if len(self._load_stats) < self._dpoints_num:
            num = self._dpoints_num - len(self._load_stats)
            stats_begin = []
            FMT = '%Y-%m-%d %H:%M:%S'
            for i in range(0, num):
                insert_time = self._uptime - (num - i) * timedelta(seconds = self._interval)
                insert_time_str = insert_time.strftime(FMT)
                stats_begin.append({'time':insert_time_str, 'load':0})
            return stats_begin + self._load_stats
        else:
            return self._load_stats

    def key_metrics(self):
    	metrics = {'max': self._max, 'min': self._min, 'avg': self._avg}
    	return metrics

    def _generate_messages(self):
        if len(self._load_stats) >= self._min_error_dps:
            total_load = 0
            slice_begin = -1 * self._min_error_dps
            for load_data in self._load_stats[slice_begin:]:
                total_load = total_load + load_data['load']
            load_avg = float("{0:.5f}".format(total_load / float (self._min_error_dps)))
            curtime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            if load_avg >1 :
                error_message = "High load generated an alert - load = %f, triggererd at %s" % (load_avg, curtime)
                self._messages.append(error_message)
                self._overload = True
            elif self._overload:
                correct_message = "Load return to below 1 at %s" % (curtime)
                self._overload = False
                self._messages.append(correct_message)

    # return messages, most recent on top
    def get_messages(self):
        return list(reversed(self._messages))



