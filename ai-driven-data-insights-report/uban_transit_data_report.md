# Urban Transit Ridership: 2024 Data Insights Report

**Prepared for:** UrbanTransit Operations Team
**Data source:** Urban Transit Ridership Data 2024, 366 daily records covering January 1 through December 31, 2024
**Prepared with:** AI-assisted analysis, with every figure verified against a direct computation of the underlying data

---

## 1. Summary of Key Trends

**Ridership follows a strong seasonal pattern, not a random one.** Average daily ridership rises through the spring, peaks in April at about 2,480 riders a day, and falls steadily from midsummer through early autumn. The low point is October, at about 1,587 riders a day. That is a swing of roughly 36 percent between the busiest and quietest months, and it repeats a smooth curve rather than jumping around, which suggests a real seasonal driver such as weather, school terms, or tourism rather than random noise.

| Period | Average daily ridership |
| --- | --- |
| Peak months (March, April, May) | 2,330 to 2,480 |
| Trough months (August, September, October) | 1,587 to 1,673 |
| Year-round average | about 2,016 |

**Day of the week has almost no effect on ridership.** Every day of the week averages within about 60 riders of every other day, a difference of roughly 3 percent. There is no meaningful weekday commuter peak and no meaningful weekend drop in this data. Any planning that assumes a strong weekday-versus-weekend pattern would not be supported by this year of records.

**Ticket sales track ridership almost exactly.** The two figures move together on 366 out of 366 days, with a correlation of 0.99. This is expected and confirms the two columns are measuring the same underlying demand, which is a useful sanity check on the dataset itself.

**Delays do not explain changes in ridership or ticket sales.** The scenario brief asked us to look for a relationship between delays and ticket sales. After checking this directly, neither the number of daily delays nor the average delay length shows any meaningful relationship with ridership or with ticket sales across the full year. Both relationships are effectively flat. This is a genuine finding, not a gap in the analysis: delays, at the levels recorded this year, are not what is driving the seasonal decline in ridership, and any explanation for the autumn drop should be sought elsewhere.

## 2. Notable Anomalies

**A repeated value that looks like a data problem, not a real pattern.** Forty-two of the 366 days, about one day in nine, show daily ridership as exactly 1,500 riders, an oddly round number to hit that often by chance. These days are concentrated almost entirely in August through November, with September alone accounting for 17 of them. This has the signature of a floor or minimum value applied somewhere in data collection or reporting, rather than 42 separate days that all happened to reach precisely the same ridership figure. Until this is confirmed with whoever owns the data pipeline, the true size of the autumn ridership drop described above should be treated as a lower bound, not a precise number.

**A single unexplained spike.** April 23 recorded 2,958 riders, the highest single day of the year by a wide margin, well above the normal range for that time of year. It also had the largest gap between ticket sales and ridership recorded all year. This looks like a one-off event rather than part of the spring seasonal rise, and it is worth confirming whether a specific occurrence, such as a citywide event or a service disruption elsewhere in the network, took place that day.

## 3. Actionable Recommendations

1. **Confirm the 1,500-rider floor with the data team before using this dataset for planning.** Forty-two days landing on the exact same figure is very unlikely to be genuine ridership and should be verified or corrected before it is used in any forecast or budget decision.

2. **Plan staffing and service levels around the confirmed seasonal curve, not a flat annual average.** Given the roughly 36 percent gap between spring and autumn ridership, schedules built on a single year-round average will over-staff the autumn and may under-staff the spring.

3. **Do not frame delay reduction as a ridership recovery strategy.** Since delays show no measurable relationship with ridership or ticket sales in this data, any communication or investment aimed at winning back autumn ridership through fewer delays is not supported by the evidence and should be tested separately before being funded.

4. **Investigate the cause of the autumn ridership drop directly, rather than assuming a known cause.** Because neither the day of the week nor delays explain the decline, the operations team should look at other candidates, such as seasonal fare changes, service or route changes, competing transport options, or local events, using this report as the starting baseline rather than the final answer.

5. **Follow up on April 23 as a specific, dated event rather than folding it into the spring average.** Confirming what happened that day will either explain a genuine one-off demand spike worth repeating, such as a promotion or event, or reveal a data entry issue that should be corrected.

---

## 4. Prompt History

This log records how I produced the analysis, including the point where I moved away from asking an AI model to eyeball the raw data and toward asking a script to compute it directly.

### Stage One. First-Pass Exploratory Prompt

Following the scenario's suggested starting point, I began with the plain, thin version of the questions suggested in the lab brief, run together as one first-pass prompt:

```
Analyze the headers and structure of this CSV, and Identify the peak ridership day of the week based on this data. Also, Is there a correlation between the 'Delay' column and the 'Ticket Sales' column? then draft a key insight for a non-technical manager based on this finding.
```

This prompt was useful for orientation, but it still asks a language model to perform arithmetic and pattern detection across 366 rows of numbers by reading them, which is exactly the kind of task where a fluent but wrong answer is hardest for me to catch by eye. Rather than trust an eyeballed answer to the day-of-week question or the delay correlation question, I replaced both with a direct computation in the next stage.

### Stage Two. Computing the Real Numbers

Instead of asking a model to estimate monthly averages, day-of-week averages, and a delay-to-sales correlation, I ran a short script directly against the CSV to calculate:

```
For every row: parse the date, ridership, ticket sales, delay count, and average delay minutes.
Compute: average ridership per calendar month, average ridership per day of week,
the Pearson correlation between delay count and ridership, between average delay minutes
and ridership, between delay count and ticket sales, and between average delay minutes
and ticket sales, and the correlation between ridership and ticket sales.
Also compute: how many days have ridership or ticket sales at exactly 1,500, broken down
by month, and flag any day where ridership or average delay minutes is more than 2.5
standard deviations from the yearly mean.
```

This gave me the verified figures I used throughout this report: the April peak and October trough, the near-zero delay correlations, the 0.99 ridership-to-sales correlation, the 42 days at exactly 1,500 riders concentrated in August through November, and the single outlier on April 23.

### Stage Three. Turning Verified Numbers Into Plain-English Insights

With the numbers fixed and no longer in question, I wrote the next prompt to ask only for interpretation, not calculation:

```
Here are verified statistics from a transit ridership dataset: [monthly averages, day-of-week
averages, correlation values, anomaly counts]. Using only these numbers, write one plain-English,
jargon-free sentence per finding for a non-technical operations manager. Do not add any claim,
cause, or number that is not directly supported by the statistics given.
```

I checked each resulting sentence against the number it claimed to describe before I allowed it into the report. This is the step where the delay-and-sales finding took its final shape: my first-pass instinct, prompted by the scenario itself, was to look for a story connecting delays to lost ridership, and the verified correlation values did not support one. I wrote the report to say so directly instead of forcing a connection.

### Stage Four. Chaining Into Recommendations

For the final prompt, I fed the fact-checked insight list back in as fixed input and asked for only the recommendations, constrained to what the insights actually support:

```
Here are five fact-checked insights about UrbanTransit's 2024 ridership data: [insight list].
Write three to five short, scannable, actionable recommendations for an operations manager,
based only on these insights. Do not introduce a new claim about the data that is not already
in the insight list.
```

This kept the recommendations section from drifting into generic transit advice, since I required every recommendation to trace back to a specific, already-verified finding above it.

---

## 5. Reflection

The biggest challenge was resisting the pull of the scenario's own framing. The brief points directly at a delay-to-sales correlation, and it would have been easy to let a model describe a relationship that was not actually there. I avoided that by refusing to let any model calculate the correlation itself. I computed every average, every correlation coefficient, and every anomaly count directly from the CSV first, and only afterward asked a model to put verified numbers into plain English, with an explicit instruction not to add anything the numbers did not support.

That is also how I ensured accuracy: no number in the report came from a model's read of the raw data, only from direct computation, and every sentence was checked against the specific figure it described before being kept.

My prompts evolved from asking the model to find patterns to asking it to explain patterns I had already confirmed. The first-pass prompts asked the model to compute; the later ones deliberately did not, and that single change removed the risk of a plausible-sounding but wrong finding entering the final report.
