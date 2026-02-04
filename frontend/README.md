# MachWork Frontend

The frontend is a component-based, enterprise-grade web UI with responsive layouts for desktop, tablet, and mobile. It is structured to support dark/light themes, RBAC-driven navigation, and modular feature delivery.

## Folder Structure

```
src/
  app/            # Application root, routing, providers
  assets/         # Static assets (logos, fonts, icons)
  components/     # Reusable UI components
  features/       # Feature modules (auth, projects, invoices, etc.)
  hooks/          # Shared React hooks or framework equivalents
  pages/          # Route-aligned pages
  services/       # API client, auth, and data services
  styles/         # Global styles and theme tokens
  tests/          # UI and integration tests
```

## UX Principles

- Professional construction-focused aesthetic.
- KPI dashboards with clear data hierarchies.
- Strict RBAC gating for navigation and actions.
- Accessibility and localization-ready components.

See `docs/` for API contracts and role permissions.
