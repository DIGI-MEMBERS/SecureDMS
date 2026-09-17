import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";

import Login from "./pages/Login";
import OTP from "./pages/OTP";
import Dashboard from "./pages/Dashboard";
import Cases from "./pages/Cases";
import CaseDetails from "./pages/CaseDetails";
import Documents from "./pages/Documents";
import UploadDocument from "./pages/UploadDocument";
import VersionHistory from "./pages/VersionHistory";
import AuditLogs from "./pages/AuditLogs";
import Layout from "./components/Layout";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
  return (
    <BrowserRouter>
  <Routes>

    <Route path="/login" element={<Login />} />

    <Route path="/otp" element={<OTP />} />

    <Route
      path="/dashboard"
      element={
        <ProtectedRoute>
  <Layout>
    <Dashboard />
  </Layout>
</ProtectedRoute>
      }
    />

    <Route
      path="/cases"
      element={
        <ProtectedRoute>
  <Layout>
    <Cases />
  </Layout>
</ProtectedRoute>
      }
    />

    <Route
  path="/cases/:id"
  element={
    <ProtectedRoute>
      <Layout>
        <CaseDetails />
      </Layout>
    </ProtectedRoute>
  }
/>

<Route
  path="/documents"
  element={
    <ProtectedRoute>
      <Layout>
        <Documents />
      </Layout>
    </ProtectedRoute>
  }
/>

<Route
  path="/documents/upload"
  element={
    <ProtectedRoute>
      <Layout>
        <UploadDocument />
      </Layout>
    </ProtectedRoute>
  }
/>

<Route
  path="/documents/:id/versions"
  element={
    <ProtectedRoute>
      <Layout>
        <VersionHistory />
      </Layout>
    </ProtectedRoute>
  }
/>

<Route
  path="/audit-logs"
  element={
    <ProtectedRoute>
      <Layout>
        <AuditLogs />
      </Layout>
    </ProtectedRoute>
  }
/>



    <Route
      path="*"
      element={<Navigate to="/login" replace />}
    />

  </Routes>
</BrowserRouter>
  );
}

export default App;