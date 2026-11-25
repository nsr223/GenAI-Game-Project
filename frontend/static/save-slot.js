export const slot = "beneath-the-surface.save.v1";
const ownerKey = slot + ".owner";
const tabKey = slot + ".tab";

export class StorageUnavailable extends Error {
  constructor(cause) {
    const full = cause?.name === "QuotaExceededError";
    super(full
      ? "Browser storage is full. Free some space and retry, or play this session without saving."
      : "Browser storage is blocked or unavailable. Allow site storage and retry, or play this session without saving.", {cause});
  }
}

function storage(operation) {
  try {
    return operation();
  } catch (cause) {
    throw new StorageUnavailable(cause);
  }
}

export const readSave = () => storage(() => localStorage.getItem(slot));
export const writeSave = (save) => storage(() => localStorage.setItem(slot, save));
export const isSlotChange = (key) => key === slot || key === ownerKey || key === null;

// IndexedDB serializes ownership and saves across tabs on plain HTTP too.
// Mirror changes to localStorage for storage events and compatibility with the existing slot.
export function openFallback() {
  const id = Array.from(crypto.getRandomValues(new Uint32Array(4))).join("-");
  const previous = storage(() => sessionStorage.getItem(tabKey));
  const reloading = performance.getEntriesByType("navigation")[0]?.type === "reload";
  let opening;

  function open() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(slot, 1);
      request.onupgradeneeded = () => request.result.createObjectStore("coordination");
      request.onsuccess = () => {
        const db = request.result;
        db.onversionchange = () => { db.close(); opening = undefined; };
        resolve(db);
      };
      request.onerror = () => reject(request.error);
    });
  }

  async function coordinate(operation) {
    try {
      opening ??= open().catch(cause => { opening = undefined; throw cause; });
      const db = await opening;
      return await new Promise((resolve, reject) => {
        const transaction = db.transaction("coordination", "readwrite");
        const store = transaction.objectStore("coordination");
        const request = store.get("slot");
        let result;
        transaction.oncomplete = () => resolve(result);
        transaction.onabort = () => reject(transaction.error);
        request.onsuccess = () => {
          try {
            const record = request.result ?? {owner: null, save: localStorage.getItem(slot)};
            result = operation(record, () => store.put(record, "slot"));
          } catch (cause) {
            reject(cause);
            transaction.abort();
          }
        };
      });
    } catch (cause) {
      throw new StorageUnavailable(cause);
    }
  }

  return {
    read: ({initial = false, takeover = false} = {}) => coordinate((record, update) => {
      if (record.owner !== id && (takeover || (initial && (
        record.owner === null || (reloading && record.owner === previous)
      )))) {
        // Recognize a reload without giving a duplicated tab the same document ID.
        try { sessionStorage.setItem(tabKey, id); } catch { /* Explicit takeover still works. */ }
        localStorage.setItem(ownerKey, id);
        record.owner = id;
        update();
      } else if (initial && record.owner !== id) {
        try { sessionStorage.removeItem(tabKey); } catch { /* Session storage is optional here. */ }
      }
      return {stored: record.save, writable: record.owner === id};
    }),
    commit: (expected, save, current = () => true) => coordinate((record, update) => {
      if (!current() || record.owner !== id || record.save !== expected) return false;
      localStorage.setItem(slot, save);
      record.save = save;
      update();
      return true;
    }),
    release: () => coordinate((record, update) => {
      if (record.owner !== id) return;
      localStorage.removeItem(ownerKey);
      record.owner = null;
      update();
    }),
  };
}
