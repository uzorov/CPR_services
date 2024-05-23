FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build

WORKDIR /src

COPY ["./notification-service/NotificationService/NotificationService.csproj", "NotificationService/"]
RUN dotnet restore "NotificationService/NotificationService.csproj"

COPY ./notification-service/NotificationService/ "NotificationService/"

WORKDIR /src/NotificationService

RUN dotnet publish -c Release -o /app/out

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime

WORKDIR /app

COPY --from=build /app/out .

EXPOSE 82

ENTRYPOINT ["dotnet", "NotificationService.dll", "--urls", "http://0.0.0.0:82"]
