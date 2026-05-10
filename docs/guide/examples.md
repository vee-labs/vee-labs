# Examples

A growing collection of usage examples for Vee Labs projects.

## Basic usage

```typescript
import { initialize } from '@vee-labs/core'

await initialize({
  debug: true,
  environment: 'development',
})
```

## Logging

```typescript
import { logger } from '@vee-labs/utils'

logger.info('Application started')
logger.warn('Cache miss for key: user:42')
logger.error('Failed to connect to upstream', { retry: 3 })
```

## Validation

```typescript
import { validator } from '@vee-labs/utils'

if (!validator.email(input)) {
  throw new Error('Invalid email')
}
```

## Event handling

```typescript
import { events } from '@vee-labs/core'

events.on('ready', () => {
  console.log('System is ready')
})
```

More examples will be added as new modules are released. Have one to contribute? See the [contributing guide](./contributing.md).
