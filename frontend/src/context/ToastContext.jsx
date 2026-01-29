import { createContext, useContext, useState, useCallback } from "react";

const ToastContext = createContext();

export const ToastProvider = ({ children }) => {
  const [toast, setToast] = useState(null);

  const showToast = useCallback((message, type = "danger") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 4000); // auto-hide
  }, []);

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {toast && <Toast message={toast.message} type={toast.type} />}
    </ToastContext.Provider>
  );
};

export const useToast = () => useContext(ToastContext);

const Toast = ({ message, type }) => (
  <div
    className={`toast align-items-center text-bg-${type} show position-fixed bottom-0 end-0 m-4 shadow`}
    role="alert"
    style={{ zIndex: 9999, minWidth: "300px" }}
  >
    <div className="d-flex">
      <div className="toast-body">{message}</div>
      <button
        type="button"
        className="btn-close btn-close-white me-2 m-auto"
        onClick={() => {}}
      />
    </div>
  </div>
);
