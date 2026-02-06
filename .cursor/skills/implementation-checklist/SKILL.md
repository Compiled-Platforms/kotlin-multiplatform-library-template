---
name: implementation-checklist
description: Create structured implementation plans with phases, steps, deliverables, tests, and success criteria. Use when planning features, breaking down tasks, creating roadmaps, or when the user asks for an implementation plan, checklist, or asks to structure a large task.
---

# Implementation Checklist

Create comprehensive, testable implementation plans that break complex features into manageable steps.

## When to Use

- User asks to plan a feature implementation
- User wants to break down a large task
- User requests an implementation roadmap or checklist
- You identify a task that needs structured planning (3+ major components)

## Structure

### Overall Format

```markdown
# [Feature Name] - Implementation Plan

## Overview
Brief description of the feature and its goals.

## Phases

### Phase 1: [Phase Name] (X steps)

#### Step X.Y: [Step Name]
Brief description of what this step accomplishes.

**Deliverables:**
- [ ] Specific file or component to create
- [ ] Another deliverable with concrete output
- [ ] Implementation details (specific functions, classes, etc.)

**Tests:**
- [ ] Specific test scenario to verify
- [ ] Another test scenario
- [ ] Edge cases to cover

**Success Criteria:** [Clear definition of done for this step]

---
```

## Key Principles

### 1. Testable Steps

Every step should have:
- **Concrete deliverables** (files, classes, functions)
- **Specific tests** (not "add tests" but "test concurrent access", "test error handling for X")
- **Clear success criteria** (measurable, like "all tests pass" or "API returns expected response")

### 2. Small But Not Micro

- **Too large**: "Implement entire authentication system"
- **Too small**: "Add import statement for User class"
- **Just right**: "Implement JWT token validation with expiry checking"

Aim for steps that:
- Can be completed in one focused session
- Have clear input/output
- Can be tested independently when possible

### 3. Progressive Complexity

Order steps so that:
- Foundation pieces come first (data models, interfaces)
- Core logic comes next (business logic, algorithms)
- Integration comes after (platform-specific, UI)
- Polish comes last (documentation, samples, optimization)

### 4. Track Progress

As steps complete:
- Change `[ ]` to `[x]` for completed items
- Add **implementation notes** under completed steps
- Document **test results** (e.g., "✅ All 15 tests pass")
- Update **success criteria** with actual results

## Template Sections

### Deliverables Section

List specific, verifiable outputs:

```markdown
**Deliverables:**
- [x] `UserRepository.kt` with CRUD operations
- [x] `UserRepositoryImpl.kt` implementing thread-safe storage
- [x] Error handling for network failures
- [x] Retry logic with exponential backoff
- [x] Connection pooling configuration
```

### Tests Section

List specific test scenarios:

```markdown
**Tests:**
- [x] Save user returns success for valid data
- [x] Save user returns error for duplicate email
- [x] Concurrent saves don't corrupt data
- [x] Network timeout triggers retry with backoff
- [x] Retry exhaustion returns final error
- [x] Connection pool limits concurrent requests
```

### Success Criteria

Clear, measurable definition of done:

```markdown
**Success Criteria:** ✅ Repository saves/loads users correctly, all 25 tests pass, thread-safe verified with 100 concurrent operations
```

## Phases Organization

Organize into logical phases:

```markdown
### Phase 1: Foundation (3 steps)
- Data models
- Storage interfaces
- Configuration

### Phase 2: Core Logic (4 steps)
- Business rules
- Validation
- State management
- Error handling

### Phase 3: Platform Integration (3 steps)
- Android implementation
- iOS implementation
- JVM implementation

### Phase 4: Polish (2 steps)
- Sample application
- Documentation
```

## Example: Small Feature

```markdown
# Email Validation - Implementation Plan

## Overview
Add comprehensive email validation with format checking and disposable email detection.

## Steps

### Step 1: Email Format Validator
Basic RFC-compliant email validation.

**Deliverables:**
- [ ] `EmailValidator.kt` with regex pattern matching
- [ ] Support for common TLDs and international characters
- [ ] Whitespace trimming and normalization

**Tests:**
- [ ] Valid emails pass (user@example.com)
- [ ] Invalid formats fail (no @, missing domain)
- [ ] Edge cases (unicode, subdomain, plus addressing)
- [ ] Performance (10000 validations < 100ms)

**Success Criteria:** Validates emails per RFC 5322, all tests pass

---

### Step 2: Disposable Email Detection
Block temporary/disposable email providers.

**Deliverables:**
- [ ] `DisposableEmailDetector.kt` with provider list
- [ ] 1000+ known disposable domains
- [ ] Efficient lookup (HashSet, O(1))

**Tests:**
- [ ] Known disposable domains detected (guerrillamail.com)
- [ ] Valid providers allowed (gmail.com, outlook.com)
- [ ] Case-insensitive matching
- [ ] Subdomain handling

**Success Criteria:** Detects disposable emails, lookup < 1ms

---

### Step 3: Integration
Combine validators into unified API.

**Deliverables:**
- [ ] `EmailValidationService` facade
- [ ] Combined validation (format + disposable)
- [ ] Clear error messages for each failure type

**Tests:**
- [ ] End-to-end validation flow
- [ ] Error message clarity
- [ ] Performance benchmarks

**Success Criteria:** Single validation API, all tests pass
```

## Updating Plans

As you work:

1. **Mark completed items**: Change `[ ]` to `[x]`
2. **Add implementation notes**: Details about decisions made, gotchas encountered
3. **Update success criteria**: Add actual results (test counts, performance numbers)
4. **Document deviations**: Explain any changes from original plan

Example of completed step:

```markdown
#### Step 1.1: Email Format Validator ✅ COMPLETE

**Deliverables:**
- [x] `EmailValidator.kt` with regex pattern matching
- [x] Support for common TLDs and international characters
- [x] Whitespace trimming and normalization
- [x] Implemented with Kotlin Regex (platform-agnostic)

**Implementation Notes:**
- Used RFC 5322 simplified pattern for KMP compatibility
- Added extension function `String.isValidEmail()` for convenience
- Normalization handles leading/trailing spaces and case

**Tests:**
- [x] 15 comprehensive tests in EmailValidatorTest
- [x] Valid email formats (50+ examples)
- [x] Invalid formats (30+ edge cases)
- [x] Unicode support verified
- [x] Performance: 10000 validations in 45ms

**Success Criteria:** ✅ Validates emails per RFC 5322, all 15 tests pass
```

## Anti-Patterns

### Vague Deliverables
❌ **Bad**: "Add authentication"  
✅ **Good**: "Implement `AuthService.kt` with login(), logout(), and validateToken()"

### Generic Tests
❌ **Bad**: "Add tests"  
✅ **Good**: "Test login with valid credentials, invalid password, expired token"

### Unclear Success
❌ **Bad**: "Authentication works"  
✅ **Good**: "Users can login/logout, tokens expire after 1 hour, all 12 tests pass"

## Tips

1. **Start with overview**: Brief feature description and goals
2. **Break into phases**: Group related steps (Foundation, Core, Integration, Polish)
3. **Name phases clearly**: Use descriptive names, not just "Phase 1"
4. **Number steps**: Use X.Y format (Phase.Step) for easy reference
5. **Be specific**: Concrete deliverables, not abstract concepts
6. **Make testable**: Every step should have verifiable tests
7. **Update continuously**: Mark progress, add notes, document deviations

## Common Phase Patterns

**Foundation Phase**: Data models, interfaces, configuration  
**Core Logic Phase**: Business rules, algorithms, state management  
**Platform Phase**: Platform-specific implementations (Android, iOS, JVM)  
**Integration Phase**: Wiring components together, orchestration  
**Sample Phase**: Demo applications, examples  
**Documentation Phase**: API docs, user guides, README  
**Polish Phase**: Performance optimization, edge cases, final cleanup

## Implementation Order Summary

At the end of the plan, include a summary section:

```markdown
## Implementation Order Summary

**Total Steps: ~18-20**

1. **Phase 1 (Foundation)**: 3 steps - Core types, interfaces, storage
2. **Phase 2 (Business Logic)**: 5 steps - Throttling, sentiment, strategies
3. **Phase 3 (Platform)**: 3 steps - Android, iOS, JVM implementations
4. **Phase 4 (Manager)**: 2 steps - Manager, singleton factory
5. **Phase 5 (Sample App)**: 3 steps - Basic UI, advanced features, testing
6. **Phase 6 (Documentation)**: 2 steps - API docs, user guides
7. **Phase 7 (Integration)**: 1 step - Project setup, publishing

**Estimated Total:** ~20 well-defined, testable steps.

Each step is:
- ✅ Independently testable
- ✅ Builds on previous work
- ✅ Has clear deliverables and success criteria
- ✅ Small enough to complete in focused session
- ✅ Large enough to make meaningful progress
```

This summary provides:
- **Quick overview** of total scope
- **Phase breakdown** with step counts
- **Phase descriptions** (one-line summaries)
- **Step characteristics** (what makes them good steps)

Benefits:
- Helps stakeholders understand scope at a glance
- Shows logical progression through phases
- Demonstrates thoughtful step sizing
- Sets expectations for total effort
