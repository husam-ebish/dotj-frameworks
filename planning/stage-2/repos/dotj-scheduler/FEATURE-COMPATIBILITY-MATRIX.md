# DJ-030 .j Scheduler: feature compatibility matrix

Quartz.NET behavior is the source; do not reuse Java Quartz. Preserve DST/misfire semantics explicitly and compare time-zone data versions.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Jobs triggers and calendars | Proposed Java contracts: JobKey, TriggerKey, CalendarExclusion | DST gaps/overlaps have fixture-backed outcomes; invalid cron fails with location; calendars do not silently change timezone | Planned; evidence gates open |
| WP-02 | Misfires scheduling and clocks | Proposed Java contracts: NextFireTime, MisfireInstruction, SchedulerClock | Restart after downtime produces the documented firing sequence; clock adjustments do not spin indefinitely; pause/resume retains policy | Planned; evidence gates open |
| WP-03 | Persistent store and clustering | Proposed Java contracts: TriggerStore, SchedulerInstance, AcquisitionLease | Concurrent nodes do not acquire one occurrence twice under declared store guarantees; recovery does not claim exactly-once side effects | Planned; evidence gates open |
| WP-04 | Execution listeners and lifecycle | Proposed Java contracts: JobExecutionContext, Listener, InterruptRequest | Listener failure cannot leak a worker; nonconcurrent jobs serialize correctly; interrupt remains cooperative and observable | Planned; evidence gates open |
| WP-05 | Adapters and verification | Proposed Java contracts: StoreAdapter, ScheduleTrace, ManagementApi | Core schedule calculation works without a database; test traces identify timezone data version; every claimed store has recovery evidence | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Persistent schema/version compatibility and supported cron dialect require decisions; job execution should not depend on jobs repo.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
