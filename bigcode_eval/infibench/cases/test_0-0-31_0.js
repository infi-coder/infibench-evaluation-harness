
const __test_assert = require('node:assert');

function handle_null_b(obj) {
    return "NULLOBJ!"
}

oo = false;

__test_assert.strictEqual(test(oo, handle_null_b), false);

ooo = "";

__test_assert.strictEqual(test(ooo, handle_null_b), "");

