# DJ-016 .j Auth: feature compatibility matrix

Preserve protocol rules and event ordering; Java APIs adapt async and storage abstractions. No compliance claim from happy-path token issuance.

| Package | Retained capability | Adaptation | Required observable behavior | Status |
|---|---|---|---|---|
| WP-01 | Protocol model and event pipeline | Proposed Java contracts: ProtocolRequest, ProtocolError, HandlerDescriptor | Duplicate security parameters are rejected consistently; handlers execute in declared order; unsupported grants return explicit protocol errors | Planned; evidence gates open |
| WP-02 | Authorization server and token lifecycle | Proposed Java contracts: AuthorizationTransaction, GrantRecord, TokenRecord | Codes cannot be redeemed twice; redirect matching is exact per profile; replayed refresh tokens follow declared family-revocation policy | Planned; evidence gates open |
| WP-03 | Client discovery and login state | Proposed Java contracts: ClientRegistration, LoginState, DiscoveryDocument | Cross-session callbacks fail; unexpected issuers fail closed; discovery refresh cannot downgrade transport or algorithm policy | Planned; evidence gates open |
| WP-04 | JOSE and resource validation | Proposed Java contracts: JoseHeader, ValidationPolicy, KeyResolver | Algorithm/key-type confusion and unsigned tokens fail; malformed critical headers fail; key refresh is bounded under attacker-supplied IDs | Planned; evidence gates open |
| WP-05 | Stores web integration and conformance | Proposed Java contracts: AuthorizationStore, TokenStore, AuthWebAdapter | Concurrent redemption is serialized by storage contract; secrets are redacted; protocol claims identify exact tested profiles and unresolved certification | Planned; evidence gates open |

## Claim rules

API spelling compatibility, behavioral compatibility, protocol/file-format interoperability and deployment-platform support are separate profiles. Java contracts are proposals; they are not upstream class declarations. No CLR assembly compatibility is claimed. A feature becomes supported only after its mapped fixtures pass on the declared versions/platforms and remaining deviations are published. A feasibility failure keeps the feature visible with its evidence and alternatives.

## Unresolved boundaries retained

Investigate IdentityModel/JWT dependencies, supported grants, JOSE algorithms and optional certification suites. Store adapters must not create a core/entity cycle.

Full source-to-feature coverage and semantic overload mapping are E02 outputs. This matrix covers the planned capability families; it is not a false claim that every upstream public member has already been semantically audited.
