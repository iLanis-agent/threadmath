// Thread Math engine: threads per inch to pitch and back, and the turns a screw thread needs to move a distance. Exact integers, results rounded half up.
function _p(t, err, intDigits, places, lo, hi) { // decimal text -> integer scaled by 10^places
  t = typeof t === "string" ? t.trim() : "";
  var m = new RegExp("^([0-9]{1," + intDigits + "})(?:\\.([0-9]{1," + places + "}))?$").exec(t);
  if (!m) throw new Error(err);
  var v = parseInt(m[1], 10) * Math.pow(10, places) + (m[2] ? parseInt(m[2].padEnd(places, "0"), 10) : 0);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
function _w(t, err, lo, hi) {
  t = typeof t === "string" ? t.trim() : "";
  if (!/^[0-9]{1,3}$/.test(t)) throw new Error(err);
  var v = parseInt(t, 10);
  if (v < lo || v > hi) throw new Error(err);
  return v;
}
var _TPI = "the threads per inch must be from 1 to 100 with at most one decimal place";
var _PITCH = "the pitch must be from 0.05 to 10 mm with at most two decimal places";
var _LEN = "the distance must be from 0.1 to 1000 mm with at most one decimal place";
var _START = "the number of starts must be a whole number from 1 to 4";
function _hu(n, d) { return Math.floor((2 * n + d) / (2 * d)); }
function _dec(v, places) {
  var base = Math.pow(10, places);
  var s = String(Math.floor(v / base)), f = String(v % base).padStart(places, "0").replace(/0+$/, "");
  return f ? s + "." + f : s;
}
function _starts(n) { return n + (n === 1 ? " start" : " starts"); }

function tpiTruth(tpi) {
  var t = _p(tpi, _TPI, 3, 1, 10, 1000);
  return _dec(t, 1) + " threads per inch is a pitch of " + _dec(_hu(254000, t), 3) + " mm.";
}
function pitchTruth(pitch) {
  var p = _p(pitch, _PITCH, 2, 2, 5, 1000);
  return "A pitch of " + _dec(p, 2) + " mm is " + _dec(_hu(254000, p), 2) + " threads per inch.";
}
function turnsTruth(pitch, starts, dist) {
  var p = _p(pitch, _PITCH, 2, 2, 5, 1000), s = _w(starts, _START, 1, 4), l = _p(dist, _LEN, 4, 1, 1, 10000);
  var turns = _hu(1000 * l, p * s);
  return "A pitch of " + _dec(p, 2) + " mm with " + _starts(s) + " advances " + _dec(p * s, 2) + " mm a turn, so " + _dec(l, 1) + " mm takes " + (turns === 0 ? "under 0.01 turns" : _dec(turns, 2) + (turns === 100 ? " turn" : " turns")) + ".";
}
