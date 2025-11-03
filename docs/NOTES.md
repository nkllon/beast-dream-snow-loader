# Development Notes & Observations

## ServiceNow Plugin Installation Time

**Observation (2025-11-03):** CMDB CI Class Models plugin installation takes **significantly longer** than actual development work.

**Context:**
- Plugin installation: ~8% after several minutes (still in progress)
- Actual development: Complete MVP in single session
- All code written, tested, documented, and ready for PyPI

**Lesson:**
- Development can be very fast when infrastructure is ready
- External dependencies (ServiceNow plugin installation) are the bottleneck
- For product manager reviews: "Longest step was waiting for ServiceNow plugin, not development"

**For Future:**
- Plan for plugin installation time in project timelines
- Consider pre-activating plugins in PDI templates
- Document plugin installation as a setup step, not development blocker

**Funny Reality:**
- Can develop "really, really, really fast" including everything about a product
- But waiting for ServiceNow to install a plugin takes forever
- This is why infrastructure automation matters!

## Development Velocity

**MVP Completion Time:**
- Core features: Single session
- Documentation: Complete
- Testing: All unit tests passing
- PyPI setup: Ready
- Workflows: Configured and tested

**Bottleneck:**
- ServiceNow plugin installation (external dependency)
- Not code quality, not testing, not documentation
- Just waiting for ServiceNow to do its thing

## ServiceNow Observations

**ServiceNow is Slow:**
- Plugin installation: Takes minutes (not seconds)
- UI operations: Noticeable lag
- API responses: Generally fast but can be slow on PDIs

**PDI Characteristics:**
- Free instances (good for development)
- Smallest machines in the universe (probably)
- Plugin installation is slow but works
- Worth the wait for free development environment

## Product Management Notes

**If this were a product manager review:**
- Development: Fast ✅
- Testing: Complete ✅
- Documentation: Comprehensive ✅
- Deployment: Ready ✅
- **Bottleneck: External dependency (ServiceNow plugin installation)**

**Key Insight:**
- Development velocity is high when infrastructure is ready
- External dependencies (like ServiceNow) are the real bottlenecks
- Automation and pre-configuration can help, but some things just take time

## Development Philosophy

**"Go Slow, Verify Evidence"** - But when everything is ready, development can be very fast.

**The Reality:**
- Fast development when infrastructure is ready
- Slow when waiting for external systems
- Balance: Prepare infrastructure, then develop quickly
- Don't blame development for infrastructure delays

