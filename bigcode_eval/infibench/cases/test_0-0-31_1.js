
const __test_assert = require('node:assert');

function handle_null_b(obj) {
    return "NULLOBJ!"
}

oo = null;

__test_assert.strictEqual(test(oo, handle_null_b), "NULLOBJ!");
