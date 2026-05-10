# API Reference

## Core Modules

### Module: Core

The core module provides foundational functionality for all Vee Labs projects.

\`\`\`typescript
import { initialize, config } from '@vee-labs/core'

// Initialize with configuration
await initialize({
  debug: true,
  environment: 'development',
})
\`\`\`

#### Functions

- **\`initialize(config: Config): Promise<void>\`** - Initialize the system
- **\`config(options: ConfigOptions): void\`** - Configure settings
- **\`getVersion(): string\`** - Get current version

### Module: Utils

Utility functions for common operations.

\`\`\`typescript
import { logger, validator, parser } from '@vee-labs/utils'

logger.info('Application started')
const isValid = validator.email('test@example.com')
const data = parser.json(jsonString)
\`\`\`

#### Available Utilities

- Logger - Logging with multiple levels
- Validator - Input validation
- Parser - Data parsing and transformation

## Events

Subscribe to system events:

\`\`\`typescript
import { events } from '@vee-labs/core'

events.on('ready', () => {
  console.log('System is ready')
})

events.on('error', (error) => {
  console.error('Error occurred:', error)
})
\`\`\`

## Error Handling

All errors inherit from \`VeeLabsError\`:

\`\`\`typescript
try {
  await initialize(config)
} catch (error) {
  if (error instanceof VeeLabsError) {
    console.error(\`Error code: \${error.code}\`)
  }
}
\`\`\`